import httpx
import csv
from datetime import datetime
from zoneinfo import ZoneInfo
##https://ai.google.dev/gemini-api/docs/get-started

def convert_to_swedish_time(utc_time_str: str,) -> str:
    utc_time = datetime.fromisoformat(utc_time_str.replace("Z", "+00:00"))
    local_time = utc_time.astimezone(ZoneInfo('Europe/Stockholm'))
    return local_time.strftime("%Y-%m-%d %H:%M:%S")

class Weather:
    def __init__(self, url: str):
        self.url = url

    async def get_weather(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.url)
                if response.status_code != 200:
                    print(f"Error fetching weather data: {response.status_code}")
                    return None
                raw_data = response.json()

            time_series = raw_data["timeSeries"]
            path = "src/whats_the_weather/weather.csv"
            with open(path, "w", newline="") as f:
                fieldnames = ["time"] + list(time_series[0]["data"].keys())
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for entry in time_series:
                    row = {"time": convert_to_swedish_time(entry["time"]), **entry["data"]}
                    writer.writerow(row)
            print(f"Weather data saved to {path}")
            return raw_data
        except httpx.RequestError as e:
            print(f"An error occurred while requesting weather data: {e}")