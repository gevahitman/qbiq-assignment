# Weather Proxy Service

## Overview

REST API that proxies Open-Meteo weather data.

Built with:
- Python 3.11
- FastAPI
- Redis
- Docker
- GitHub Actions

---

## Run Locally

Install dependencies:
pip install -r requirements.txt

Open:
http://localhost:8000/docs

---

## Run With Docker
docker compose up --build

---

## Endpoints

GET /weather?city={city-name}  
GET /health

---

## Architecture

Client → FastAPI → Middleware → WeatherProvider
→ GeocodingProvider → OpenMeteoProvider → Redis Cache  

---

## Improvements

- Move classes objects creation into different location.
- Add OpenTelemetry tracing
- Add circuit breaker
