from fastapi import APIRouter, HTTPException
from app.services.weather_service import WeatherService
from app.cache.redis_cache import redis_client
from app.providers.open_meteo_provider import open_meteo_provider
from app.providers.geocoding_provider import geocoding_provider


router = APIRouter()
service = WeatherService(redis_client, open_meteo_provider, geocoding_provider)


@router.get("/weather")
async def get_weather(city: str):
    try:
        return await service.get_weather(city)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=503, detail="Weather provider unavailable")


@router.get("/health")
async def health():
    try:
        await redis_client.ping()
        return {"status": "healthy"}
    except Exception:
        raise HTTPException(status_code=503, detail="Unhealthy")
