#[macro_use] extern crate rocket;
use rocket::fs::{FileServer, relative};

mod assets;
mod listener;

#[launch]
fn rocket() -> _ {
    rocket::build()
        .attach(assets::ImageServer::default())
        .attach(assets::DbConn::fairing())
        .attach(listener::FifoChecker::default())
        .mount("/", FileServer::from(relative!("cache")))
}
