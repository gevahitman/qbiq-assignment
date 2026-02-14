import json
from app.config import settings
from app.logger import logger


class WeatherService:
    def __init__(self, redis_cache, weather_provider, geocoding_provider):
        self.redis_cache = redis_cache
        self.weather_provider = weather_provider
        self.geocoding_provider = geocoding_provider

    async def get_weather(self, city: str):
        city_key = city.lower()

        cache_key = f"weather:{city_key}"

        cached = await self.redis_cache.get(cache_key)
        if cached:
            logger.info("cache_hit", city=city_key)
            return json.loads(cached)

        logger.info("cache_miss", city=city_key)

        latitude, longitude = await self.geocoding_provider.get_coordinates(city)

        data = await self.weather_provider.fetch_weather(latitude, longitude)

        await self.redis_cache.set(
            cache_key,
            json.dumps(data),
            ex=settings.cache_ttl_seconds,
        )

        return data
