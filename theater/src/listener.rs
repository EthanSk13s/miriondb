use rocket::fairing::{Fairing, Info, Kind};
use rocket::{Rocket, Orbit, tokio::{self, select, fs, time::Duration}};
use reqwest::Client;

use crate::assets::{self, DbConn};

#[derive(Default)]
pub struct FifoChecker {}

impl FifoChecker {
    async fn check_fifo(server: &assets::ImageServer, db: &DbConn) {
        let fifo = fs::read("wake.fifo").await;
        match fifo {
            Ok(contents) => {
                if String::from_utf8_lossy(&contents) == String::from("1") {
                    server.check_for_images(db).await;

                    fs::write("wake.fifo", "0").await
                        .expect("Cannot write to fifo.");
                }
            },
            Err(_) => { println!("Error") }
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

        tokio::spawn(async move {
            let mut interval = tokio::time::interval(Duration::from_secs(1));

            loop {
                select! {
                    _ = interval.tick() => Self::check_fifo(&server, &db).await,
                    _ = &mut shutdown => break
                }
            }
        });

    }
}