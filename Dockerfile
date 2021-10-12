# syntax=docker/dockerfile:1

FROM rust:1.54 as asset-server

WORKDIR /build

COPY theater/Cargo.toml theater/Cargo.lock theater/Rocket.toml /build/
COPY theater/src/ /build/src

RUN cargo build --release

FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

COPY config.py config.py
COPY run.py run.py
COPY mirion/ /app/mirion

RUN mkdir theater

COPY theater/cache/ /app/theater/cache
COPY --from=asset-server /build/target/release/theater /app/theater/theater
COPY --from=asset-server /build/Rocket.toml theater/Rocket.toml

COPY start.sh ./

ENTRYPOINT ["./start.sh"]
