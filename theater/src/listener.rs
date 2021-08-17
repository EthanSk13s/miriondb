use std::net::SocketAddr;
use std::str::from_utf8;
use rocket::fairing::{Fairing, Info, Kind};
use rocket::{Rocket, Orbit, tokio::{self, select, net, time::Duration}};
use reqwest::Client;

use crate::assets::{self, DbConn};

#[derive(Default)]
pub struct FifoChecker {}

impl FifoChecker {
    async fn check_fifo(server: &assets::ImageServer, db: &DbConn, stream: (net::TcpStream, SocketAddr)) {
        let data = [0 as u8; 50];
        let status = Self::handle_connection(stream.0, data);

        if status == "1" {
            server.check_for_images(db).await;
        }
    }

    fn handle_connection(client: net::TcpStream, mut data: [u8; 50]) -> String {
        match client.try_read(&mut data) {
            Ok(test) => {
                let text = from_utf8(&data[0..test]);
                match text {
                    Ok(status) => status.to_string(),
                    Err(_) => String::from("N/A")
                }
            }
            Err(_) => String::from("N/A")
        }
    }
}

#[rocket::async_trait]
impl Fairing for FifoChecker {
    fn info(&self) -> Info {
        Info {
            name: "Fifo Checker",
            kind: Kind::Liftoff
        }
    }

    async fn on_liftoff(&self, rocket: &Rocket<Orbit>) {
        let server = assets::ImageServer { client: Client::new() };
        let db = DbConn::get_one(&rocket).await
                            .expect("database mounted.");
        let mut shutdown = rocket.shutdown();
        let listener = net::TcpListener::bind("127.0.0.1:5501").await.unwrap();


        // TODO: Thread panicks when shutting down, currently does not affect anything should fix
        tokio::spawn(async move {
            let mut interval = tokio::time::interval(Duration::from_secs(1));

            loop {
                select! {
                    _ = interval.tick() => {
                            match listener.accept().await {
                                Ok(stream) => Self::check_fifo(&server, &db, stream).await,
                                Err(_) => {}
                            }
                    },
                    _ = &mut shutdown => break
                }
            }
        });

    }
}