#[macro_use] extern crate rocket;
use rocket::fs::{FileServer};

mod assets;
mod listener;

#[launch]
fn rocket() -> _ {
    rocket::build()
        .attach(assets::DbConn::fairing())
        .attach(listener::FifoChecker::default())
        .attach(assets::ImageServer::default())
        .mount("/", FileServer::from("./cache"))
}
