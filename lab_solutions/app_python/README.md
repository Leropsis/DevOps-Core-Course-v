# DevOps Info Service (FastAPI)

## Overview
A lightweight web service that reports system and runtime information for the DevOps course labs.

## Prerequisites
- Python 3.11+
- FastAPI - perfect fit for small WEB application here. It has built-in OpenAPI docs and provides modern async interface.

## Installation
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the Application
```bash
python app.py
# Or with custom config
PORT=8080 python app.py
```

## API Endpoints
- `GET /` - Service and system information
- `GET /health` - Health check

## Configuration
| Variable | Default | Description |
| --- | --- | --- |
| HOST | 0.0.0.0 | Bind address |
| PORT | 5000 | HTTP port |
| DEBUG | False | Enable auto-reload and debug logging |
