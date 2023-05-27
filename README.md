# ChatGPT-like SSE Demo

This project is mean't to be a demo of how ChatGPT receives messages and returns streams back to the client.

Start FastAPI Webserver
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

Start React Client
```bash
## Change Directory
cd client

## Install modules
npm install

## Start Client
npm run dev
```