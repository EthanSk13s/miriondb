use std::path::Path;

use hyper::header::CONTENT_TYPE;
use rocket::{Orbit, Rocket, fairing::{Fairing, Kind, Info}, tokio::{self, fs, time::Duration, select}};
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
    async fn write_image(name: String, data: Vec<u8>) {
        fs::write(name, data).await
            .expect("Something went wrong with writing the file...");
    }

    async fn write_assets(&self, url: &str, path: String) {
        if Path::new(&format!("cache/{}", path)).exists() == false {
            let image = self.client.get(url).send().await;

            match image {
                Ok(data) => {
                    match data.headers().get(CONTENT_TYPE) {
                        Some(header) => {
                            if header.to_str().unwrap() == "image/png" {
                                match data.bytes().await {
                                    Ok(bytes) => {
                                        let fp = format!("cache/{}", path); 

                                        Self::write_image(fp, bytes.to_vec()).await 
                                    },
                                    Err(_) => {}
                                }
                            }
                        }
                        None => {}
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

                let awake_bg_url = format!("{}/card_bg/{}.png", base, awake_card);
                self.write_assets(&awake_bg_url, format!("card_bg/{}.png", awake_card)).await;
            }

            for costume in x.costumes.resc_ids {
                let costume_url = format!("{}/costume_icon_ll/{}.png", base, costume);

                self.write_assets(&costume_url, format!("costumes/{}.png", costume)).await;
            }
        }
    }

    async fn check_image_health(&self, file: fs::File, name: String) {
        let size = file.metadata().await.unwrap().len();

        // Anything below 129 bytes is considered "invalid" so we redownload the image
        if size <= 129 {
            let url: Vec<&str> = name.split(&['\\', '/'][..]).collect();
            let mut base = String::new();
            let mut image= String::new(); 
    
            for string in url {
                if string == "cache" {
                    continue;
                }
                match string {
                    "card" => base = "card/".to_string(),
                    "card_bg" => base = "card_bg/".to_string(),
                    "costumes" => base = "costume_icon_ll/".to_string(),
                    "icons" => base = "icon_l/".to_string(),
                    "DO_NOT_DELETE_TO_KEEP_DIR" => continue,
                    &_ => image = string.to_string()
                }
            }

            if base == "card/" {
                image = match image.strip_suffix(".png") {
                    Some(valid) => {
                        valid.to_owned()
                    }
                    None => {
                        image
                    },
                };
            
                image.insert_str(image.len(), "_a.png");
            }

            let img_url = format!("https://storage.matsurihi.me/mltd/{}{}", base, image);
            let image = self.client.get(img_url).send().await.unwrap();

            Self::write_image(name, image.bytes().await.unwrap().to_vec()).await;
        }
    }

    async fn iterate_dir(&self) {
        let base_dir = std::fs::read_dir("cache/").unwrap();

        for dir in base_dir {
            for image in std::fs::read_dir(dir.unwrap().path()).unwrap() {
                let path = image.unwrap().path();
                let file = fs::File::open(&path).await.unwrap();

                let name = format!("{}", path.to_str().unwrap());

                self.check_image_health(file, name).await;
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
        let mut shutdown = rocket.shutdown();
        let clone = Self { client: Client::new() };

        self.check_for_images(&db).await;
        self.iterate_dir().await;

        tokio::spawn(async move {
            let mut interval = tokio::time::interval(Duration::from_secs(300));

            loop {
                select! {
                    _ = interval.tick() => clone.iterate_dir().await,
                    _ = &mut shutdown => break
                }
            }
        });
    }
}