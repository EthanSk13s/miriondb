# MirionDB
Just a simple translated database for TD. All data is from [matsurihi.me](https://api.matsurihi.me/docs/)

# Building and setup
## Setup (With Docker)
1. Clone this repo
```
git clone https://github.com/EthanSk13s/miriondb
```
2. Modify the compose file as necessary, it should work out of the box (unless relying on hosting images on your own, in that case images may take time to download)

3. Now simply start with:

```
$ docker compose build
...
$ docker compose up
```

## Setup (Manual)
**!! Prerequisites are the latest version of Rust, at least python 3.8, and a ready-to-go Postgres server !!**
1. Clone this repo
```sh
git clone https://github.com/EthanSk13s/miriondb
```

2. Install requirements and initialize a venv inside the directory
```sh
python -m venv .venv
source .venv/bin/activate           # .venv/Scripts/activate if on windows
pip install -r requirements.txt
```

3. Create a new file called db.yml and modify it as necessary:
```yml
postgres:
  user: # Your postgres user
  pass: # Your postgres password
  database: # Which database to use
# If you are actively using the asset server, leave this as is
assets:
  host: "127.0.0.1"
  port: 5501
```

4. Now start the python server:
```
python run.py
```

5. Start the asset server by:
```sh
cd theater          # traverse to the theater director
cargo run           # add the --release flag, if building through release
```