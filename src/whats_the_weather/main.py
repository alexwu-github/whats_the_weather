import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

from whats_the_weather.discord_notification import send_to_discord
from whats_the_weather.get_clothing_advice import get_clothing_advice
from whats_the_weather.getWeather import Weather

load_dotenv()

##https://ai.google.dev/gemini-api/docs/get-started

discord_webhook_url = os.getenv("DISCORD_CHANNEL_WEBHOOK_URL")

url = "https://opendata-download-metfcst.smhi.se/api/category/snow1g/version/1/geotype/point/lon/18.2282/lat/59.3086/data.json"
weather_csv_path = "src/whats_the_weather/weather.csv"


async def main(url: str):
    weather = Weather(url)
    await weather.get_weather()
    print("fetching completed")

    csv_data = await asyncio.to_thread(Path(weather_csv_path).read_text)

    advice = get_clothing_advice(csv_data)
    print(advice)

    await send_to_discord(discord_webhook_url, advice)


if __name__ == "__main__":
    asyncio.run(main(url))
