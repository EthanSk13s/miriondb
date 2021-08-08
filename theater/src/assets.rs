use std::path::Path;
use tokio::fs;

use rocket::{Orbit, Rocket, fairing::{Fairing, Kind, Info}};
use rocket::serde::{Deserialize, json};
use rocket_sync_db_pools::{database, rusqlite};
use reqwest::Client;

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

#[database("theater")]
pub struct DbConn(rusqlite::Connection);

impl DbConn {
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

    async fn query_cards(&self) -> Result<Vec<Card>, rusqlite::Error> {
        let rows = self.run(|conn| {
            let mut stmt = conn.prepare(
                                r#"SELECT resc_id, rarity, ex_type, costume_resc_ids FROM card 
                                    LEFT JOIN costume USING(resc_id)"#
                            ).expect("Invalid Syntax");

            let rows = stmt.query_and_then([],
                |row| DbConn::row_to_card(row.get(0)?, row.get(1)?,
                                  row.get(2)?, match row.get(3) {
                                                                           Ok(row) => row,
                                                                           Err(_) => String::from("")
                                                                       }));

            rows.unwrap().collect::<Result<Vec<Card>, _>>()

        }).await;
    
        rows
    }
}

#[derive(Default)]
pub struct ImageServer {
    client: Client,
}

impl ImageServer {
    async fn write_image(&self, name: String, data: Vec<u8>) {
        let path = format!("cache/{}", name);
    
        fs::write(path, data).await
            .expect("Something went wrong with writing the file...");
    }

    async fn write_assets(&self, url: &str, path: String) {
        if Path::new(&format!("cache/{}", path)).exists() == false {
            let image = self.client.get(url).send().await;
            match image {
                Ok(data) => {
                    match data.bytes().await {
                        Ok(bytes) => { self.write_image(path, bytes.to_vec()).await },
                        Err(_) => {}
                    }
                },
                Err(_) => {}
            }
        }
    }
}

#[rocket::async_trait]
impl Fairing for ImageServer {
    fn info(&self) -> Info {
        Info {
            name: "Image Server",
            kind: Kind::Liftoff
        }
    }

    async fn on_liftoff(&self, rocket: &Rocket<Orbit>) {
        println!("Checking for new images... Please wait");

        let db = DbConn::get_one(&rocket).await
                    .expect("database mounted");

        for x in db.query_cards().await.unwrap() {
            let base = "https://storage.matsurihi.me/mltd";

            // Construct filenames beforehand so it's less repetitive
            let card_file = format!("{}_0", x.resc_id);
            let awake_card = format!("{}_1", x.resc_id);

            let card_url = format!("{}/card/{}_a.png", base, card_file);
            self.write_assets(&card_url, format!("card/{}.png", card_file)).await;

            let awake_url = format!("{}/card/{}_a.png", base, awake_card);
            self.write_assets(&awake_url, format!("card/{}.png", awake_card)).await;

            let icon_url = format!("{}/icon_l/{}.png", base, card_file);
            self.write_assets(&icon_url, format!("icons/{}.png", card_file)).await;

            let icon_awake = format!("{}/icon_l/{}.png", base, awake_card);
            self.write_assets(&icon_awake, format!("icons/{}.png", awake_card)).await;

            // Download SSR backgrounds... also ignore SSR anniv. cards
            let anniv_types = vec![5, 7, 10, 13];
            if x.rarity == 4 && anniv_types.iter().any(|&ex| ex == x.ex_type) == false {
                let bg_url = format!("{}/card_bg/{}.png", base, card_file);
                self.write_assets(&bg_url, format!("card_bg/{}.png", card_file)).await;

                let awake_bg_url = format!("{}/card_bg/{}", base, awake_card);
                self.write_assets(&awake_bg_url, format!("card_bg/{}.png", awake_card)).await;
            }

            for costume in x.costumes.resc_ids {
                let costume_url = format!("{}/costume_icon_ll/{}.png", base, costume);

                self.write_assets(&costume_url, format!("costumes/{}.png", costume)).await;
            }
        }
    }
}