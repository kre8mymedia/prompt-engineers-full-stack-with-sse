# ChatGPT Clone SSE Demo

This project is mean't to be a demo of how ChatGPT receives messages and returns streams back to the client.

### Start FastAPI Webserver
```bash
## Initialize Virtual Env
python3 -m venv .venv

## Start Virtual Env
source .venv/bin/activate

## Install Dependencies
pip install -r requirements.txt

## Start Server
python3 main.py
```

### Start Docker Environment
```bash
## Start Backend in Docker
docker-compose up --build
```

### Start React Client
```bash
## Change Directory
cd client

## Install modules
yarn install

## Start Client
yarn dev
```