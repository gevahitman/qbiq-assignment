import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from app.config import settings
from app.logger import logger


class OpenMeteoProvider:
    @retry(
        stop=stop_after_attempt(settings.retry_attempts),
        wait=wait_exponential(multiplier=1, min=1, max=5),
        reraise=True,
    )
    async def fetch_weather(self, latitude: float, longitude: float):
        async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
            response = await client.get(
                settings.weather_base_url,
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": "temperature_2m",
                },
            )

            logger.info(
                "upstream_call",
                status_code=response.status_code,
            )

            response.raise_for_status()
            return response.json()


open_meteo_provider = OpenMeteoProvider()
