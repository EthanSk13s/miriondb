#[macro_use] extern crate rocket;
use rocket::fs::{FileServer, relative};
use rocket::fairing::AdHoc;

mod assets;
mod listener;

#[launch]
fn rocket() -> _ {
    rocket::build()
        .attach(AdHoc::on_ignite("asset_check", assets::download_image)) // Check if we need to download new images
        .mount("/", FileServer::from(relative!("cache")))
}
