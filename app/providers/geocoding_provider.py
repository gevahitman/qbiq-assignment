import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from app.config import settings


class GeocodingProvider:
    """
    Return the coordinates of a city.
    Send a http request to the geocoding-api to retrieve the coordinates.
    """
    @retry(
        stop=stop_after_attempt(settings.retry_attempts),
        wait=wait_exponential(multiplier=1, min=1, max=5),
        reraise=True,
    )
    async def get_coordinates(self, city: str):
        async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
            response = await client.get(settings.geocoding_base_url,
                                        params={"name": city, "count": 1})

            response.raise_for_status()
            data = response.json()

            if "results" not in data or not data["results"]:
                raise ValueError("City not found")

            result = data["results"][0]
            return result["latitude"], result["longitude"]


geocoding_provider = GeocodingProvider()
