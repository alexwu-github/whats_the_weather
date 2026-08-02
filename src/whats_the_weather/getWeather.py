import httpx
import asyncio
import csv

##https://ai.google.dev/gemini-api/docs/get-started


class Weather:
    def __init__(self, url: str):
        self.url = url

    async def fetch_weather(self):
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
                    row = {"time": entry["time"], **entry["data"]}
                    writer.writerow(row)
            print(f"Weather data saved to {path}")
            return raw_data
        except httpx.RequestError as e:
            print(f"An error occurred while requesting weather data: {e}")