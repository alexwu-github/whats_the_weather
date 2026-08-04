import csv
import io
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

import httpx

from whats_the_weather.calculate_feels_like_temp import calculate_feels_like

logger = logging.getLogger(__name__)

##https://ai.google.dev/gemini-api/docs/get-started


def convert_to_swedish_time(
    utc_time_str: str,
) -> str:
    utc_time = datetime.fromisoformat(utc_time_str)
    local_time = utc_time.astimezone(ZoneInfo("Europe/Stockholm"))
    return local_time.strftime("%Y-%m-%d %H:%M:%S")


class Weather:
    def __init__(self, url: str):
        self.url = url

    async def get_weather(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.url)
                if response.status_code != 200:
                    logger.warning(
                        f"Error fetching weather data: {response.status_code}"
                    )
                    return None
                raw_data = response.json()

            time_series = raw_data["timeSeries"]

            output = io.StringIO()
            fieldnames = ["time"] + list(time_series[0]["data"].keys()) + ["feels_like"]
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            for entry in time_series:
                row = {
                    "time": convert_to_swedish_time(entry["time"]),
                    **entry["data"],
                    "feels_like": calculate_feels_like(
                        entry["data"]["air_temperature"],
                        entry["data"]["wind_speed"],
                    ),
                }
                writer.writerow(row)
            return output.getvalue()
        except httpx.RequestError as e:
            logger.error(f"An error occurred while requesting weather data: {e}")
            return None
