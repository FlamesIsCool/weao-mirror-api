# WEAO Mirror API

This is a small Flask backend that mirrors the public WEAO API.  
It forwards requests to WEAO using the required User-Agent and returns the data through clean routes.

## Endpoints

### Exploits
- GET /api/exploits  
- GET /api/exploits/<name>

### Roblox Versions
- GET /api/versions/current  
- GET /api/versions/future  
- GET /api/versions/past  

## Requirements

pip install -r requirements.txt

## Run script

python app.py
