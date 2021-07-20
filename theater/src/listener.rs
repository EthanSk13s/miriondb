use std::error::Error;
use std::{io::{Read}, net::{TcpListener, TcpStream}};

fn handle_client(stream: TcpStream) -> Result<String, Box<Error + Send + Sync>> {
    let mut connection = stream.take(1024);

    let mut response = String::new();
    connection.read_to_string(&mut response);

    Ok(response)
}

fn start_listen() -> std::io::Result<()>{
    let listener = TcpListener::bind("http://127.0.0.1:5500/")?;

    for stream in listener.incoming() {
        handle_client(stream?);
    }

    Ok(())
}