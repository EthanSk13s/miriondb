#[macro_use] extern crate rocket;
use std::fs;
use std::env;
use rocket::fs::{FileServer};
use rocket::serde::{Deserialize};
use serde_yaml;

mod assets;
mod listener;

#[launch]
fn rocket() -> _ {
    let (host, port) = match fs::read("../db.yml") {
        Ok(yaml) => {
            let file = serde_yaml::Deserializer::from_slice(&yaml);
            let value = serde_yaml::Value::deserialize(file).unwrap();

            (String::from(
                value.get("assets")
                    .unwrap().get("host")
                    .unwrap().as_str()
                    .unwrap()
                ), value.get("assets")
                    .unwrap().get("port")
                    .unwrap().as_i64()
                    .unwrap())
        },
        Err(_) => {
            println!("Cannot load from yaml, reverting to env vars...");
            let host = match env::var("ASSETS_HOST") {
                Ok(host) => host,
                Err(_) => {
                    println!("Not detecting set variables resorting to localhost.");
                    String::from("localhost")
                }
            };

            let port = match env::var("ASSETS_PORT") {
                Ok(port) => port.parse::<i64>().unwrap(),
                Err(_) => 5501
            };

            (host, port)
        }
    };
    rocket::build()
        .attach(assets::DbConn::fairing())
        .attach(listener::FifoChecker{host, port})
        .attach(assets::ImageServer::default())
        .mount("/", FileServer::from("./cache"))
}
