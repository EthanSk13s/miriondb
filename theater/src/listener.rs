use tokio::{fs, time::Duration};

use rocket::fairing::{Fairing, Info, Kind};
use rocket::{Rocket, Orbit};

#[derive(Default)]
pub struct FifoChecker {}

#[rocket::async_trait]
impl Fairing for FifoChecker {
    fn info(&self) -> Info {
        Info {
            name: "Fifo Checker",
            kind: Kind::Liftoff
        }
    }

    async fn on_liftoff(&self, _rocket: &Rocket<Orbit>) {
        tokio::spawn(async move {
            let mut interval = tokio::time::interval(Duration::from_secs(1));

            loop {
                check_fifo().await;
                interval.tick().await;
            }
        });

    }
}

async fn check_fifo() {
    let fifo = fs::read("wake.fifo").await;
    match fifo {
        Ok(contents) => {
            if String::from_utf8_lossy(&contents) == String::from("1") {
                println!("Change!");
            }
        },
        Err(_) => { println!("Error") }
    }
}