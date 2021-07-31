use std::path::Path;
use tokio::fs;

use rocket::{Rocket, Build};
use rocket::serde::{Deserialize, json};
use reqwest::Client;

use rusqlite::Connection;

struct Card {
    resc_id: String,
    rarity: i32,
    ex_type: i32,
    costumes: Costumes
}

#[derive(Deserialize)]
#[serde(crate="rocket::serde")]
struct Costumes {
    #[serde(default)]
    resc_ids: Vec<String>
}

impl Default for Costumes {
    fn default() -> Self {
        Costumes { resc_ids: Vec::new() }
    }
}

fn establish_connection() -> Connection {
    let database_url = "../theater.db";

    Connection::open(database_url)
        .expect("The path is incorrect.")
}

async fn write_image(name: String, data: Vec<u8>) {
    let path = format!("cache/{}", name);

    fs::write(path, data).await
        .expect("Something went wrong with writing the file...");
}

fn row_to_card(resc_id: String, rarity: i32, ex_type: i32, costume_resc_ids: String) -> Result<Card, rusqlite::Error> {
    let new = costume_resc_ids.replace("'", '"'.to_string().as_str());
    let resc_ids = match json::from_str(&new) {
        Ok(ids) => ids,
        Err(_) => vec![] 
    };

    let costumes = Costumes{resc_ids};
    Ok(Card {
        resc_id,
        rarity,
        ex_type,
        costumes
    })
}

fn query_cards(conn: Connection) -> Result<Vec<Card>, rusqlite::Error> {
    let mut cards = Vec::new();
    let mut stmt = conn.prepare(
        r#"SELECT resc_id, rarity, ex_type, costume_resc_ids FROM card 
                LEFT JOIN costume USING(resc_id)"#
            ).expect("oops");

    let rows = stmt.query_and_then([],
         |row| row_to_card(row.get(0)?, row.get(1)?,
                           row.get(2)?, match row.get(3) {
                                                    Ok(row) => row,
                                                    Err(_) => String::from("")
                                                }));

    for row in rows.unwrap() {
        cards.push(row.unwrap());
    }

    Ok(cards)
}

async fn write_assets(client: &Client, url: &str, path: String) {
    if Path::new(&format!("cache/{}", path)).exists() == false {
        let image = client.get(url).send().await;
        match image {
            Ok(data) => {
                match data.bytes().await {
                    Ok(bytes) => { write_image(path, bytes.to_vec()).await },
                    Err(_) => {}
                }
            },
            Err(_) => {}
        }
    }
}

pub async fn download_image(rocket: Rocket<Build>) -> Rocket<Build> {
    let client = Client::new();

    let conn = establish_connection();

    println!("Checking for new images... Please wait");
    for x in query_cards(conn).unwrap() {
        let base = "https://storage.matsurihi.me/mltd";

        // Construct filenames beforehand so it's less repetitive
        let card_file = format!("{}_0", x.resc_id);
        let awake_card = format!("{}_1", x.resc_id);

        let card_url = format!("{}/card/{}_a.png", base, card_file);
        write_assets(&client, &card_url, format!("card/{}.png", card_file)).await;

        let awake_url = format!("{}/card/{}_a.png", base, awake_card);
        write_assets(&client, &awake_url, format!("card/{}.png", awake_card)).await;

        let icon_url = format!("{}/icon_l/{}.png", base, card_file);
        write_assets(&client, &icon_url, format!("icons/{}.png", card_file)).await;

        let icon_awake = format!("{}/icon_l/{}.png", base, awake_card);
        write_assets(&client, &icon_awake, format!("icons/{}.png", awake_card)).await;

        // Download SSR backgrounds... also ignore SSR anniv. cards
        let anniv_types = vec![5, 7, 10, 13];
        if x.rarity == 4 && anniv_types.iter().any(|&ex| ex == x.ex_type) == false {
            let bg_url = format!("{}/card_bg/{}.png", base, card_file);
            write_assets(&client, &bg_url, format!("card_bg/{}.png", card_file)).await;

            let awake_bg_url = format!("{}/card_bg/{}", base, awake_card);
            write_assets(&client, &awake_bg_url, format!("card_bg/{}.png", awake_card)).await;
        }

        for costume in x.costumes.resc_ids {
            let costume_url = format!("{}/costume_icon_ll/{}.png", base, costume);

            write_assets(&client, &costume_url, format!("costumes/{}.png", costume)).await;
        }
    }

    rocket
}
