use std::path::Path;

use rocket::{Orbit, Rocket, fairing::{Fairing, Kind, Info}, tokio::fs};
use rocket::serde::{Deserialize, json};
use rocket_sync_db_pools::{database, postgres};
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
#[derive(Clone)]
pub struct DbConn(postgres::Client);

impl DbConn {
    fn row_to_card(resc_id: String, rarity: i32, ex_type: i32, costume_resc_ids: String) -> Result<Card, postgres::Error> {
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

    async fn query_cards(&self) -> Result<Vec<Card>, postgres::Error> {
        let rows = self.run(|conn| {
            let mut cards = Vec::new();
            let rows = conn.query(
                                r#"SELECT resc_id, rarity, ex_type, costume_resc_ids FROM card 
                                    LEFT JOIN costume USING(resc_id)"#, &[]
                            ).expect("Invalid Syntax");
            
            for row in rows {
                let card = DbConn::row_to_card(row.get("resc_id"), row.get("rarity"),
                                    row.get("ex_type"), match row.try_get("costume_resc_ids") {
                                        Ok(row) => row,
                                        Err(_) => String::from("")
                                    }).unwrap();
                cards.push(card);
            }
            
            cards

        }).await;
    
        Ok(rows)
    }
}

#[derive(Default)]
pub struct ImageServer {
    pub client: Client,
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

    async fn batch_write(&self, urls: Vec<String>, paths: Vec<String>) {
        for item in urls.iter().zip(paths.iter()) {
            self.write_assets(item.0, item.1.to_string()).await;
        }
    }

    pub async fn check_for_images(&self, db: &DbConn) {
        println!("Checking for new images... Please wait");

        for x in db.query_cards().await.unwrap() {
            let base = "https://storage.matsurihi.me/mltd";

            // Construct filenames beforehand so it's less repetitive
            let card_file = format!("{}_0", x.resc_id);
            let awake_card = format!("{}_1", x.resc_id);

            let urls = vec![
                format!("{}/card/{}_a.png", base, card_file),
                format!("{}/card/{}_a.png", base, awake_card),
                format!("{}/icon_l/{}.png", base, card_file),
                format!("{}/icon_l/{}.png", base, awake_card)
            ];

            let paths = vec![
                format!("card/{}.png", card_file),
                format!("card/{}.png", awake_card),
                format!("icons/{}.png", card_file),
                format!("icons/{}.png", awake_card)
            ];

            self.batch_write(urls, paths).await;

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

#[rocket::async_trait]
impl Fairing for ImageServer {
    fn info(&self) -> Info {
        Info {
            name: "Image Server",
            kind: Kind::Liftoff
        }
    }

    async fn on_liftoff(&self, rocket: &Rocket<Orbit>) {
        let db = DbConn::get_one(&rocket).await
                    .expect("database mounted.");

        self.check_for_images(&db).await;
    }
}