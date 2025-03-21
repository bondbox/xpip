FROM ubuntu:latest as builder

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y git python3-pip && apt-get clean && rm -rf /var/lib/apt/lists/* && \
    bash buildx.sh && pip cache purge && rm -rf /app/*
