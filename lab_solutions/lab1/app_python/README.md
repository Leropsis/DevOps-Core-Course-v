# DevOps Info Service (FastAPI)

[![python-ci](https://github.com/<username>/<repo>/actions/workflows/python-ci.yml/badge.svg)](https://github.com/<username>/<repo>/actions/workflows/python-ci.yml)

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

## Testing
```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest
```

## Linting
```bash
ruff check .
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

## Docker

### Building the Image
```bash
docker build -t chupapupa/devops-info-service:latest .
```

### Running the Container
```bash
docker run -p 5000:5000 chupapupa/devops-info-service:latest
# With custom port
docker run -p 8080:5000 -e PORT=5000 chupapupa/devops-info-service:latest
```

### Pulling from Docker Hub
```bash
docker pull chupapupa/devops-info-service:latest
docker run -p 5000:5000 chupapupa/devops-info-service:latest
```
