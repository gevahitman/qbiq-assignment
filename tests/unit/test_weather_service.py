import pytest
from app.services.weather_service import WeatherService


class FakeRedis:
    async def get(self, key):
        return '{"temp": 20}'

    async def set(self, key, value, ex):
        pass


class FakeGeo:
    async def get_coordinates(self, city):
        return 1, 1


class FakeWeather:
    async def fetch_weather(self, lat, lon):
        return {"temp": 99}


@pytest.mark.asyncio
async def test_cache_hit():
    service = WeatherService(
        FakeRedis(), FakeWeather(), FakeGeo(),
    )

    result = await service.get_weather("London")

    assert result == {"temp": 20}


@pytest.mark.asyncio
async def test_cache_miss():
    class EmptyRedis:
        async def get(self, key):
            return None

        async def set(self, key, value, ex):
            self.saved = value

    redis = EmptyRedis()

    service = WeatherService(
        redis, FakeWeather(), FakeGeo(),
    )

    result = await service.get_weather("London")

    assert result == {"temp": 99}
    assert redis.saved is not None
