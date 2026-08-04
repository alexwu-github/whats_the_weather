import asyncio
import logging
import os

from dotenv import load_dotenv

from whats_the_weather.discord_notification import send_to_discord
from whats_the_weather.get_clothing_advice import get_clothing_advice
from whats_the_weather.get_weather import Weather
from whats_the_weather.scheduler import start_scheduler

load_dotenv()

##https://ai.google.dev/gemini-api/docs/get-started

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

discord_webhook_url = os.getenv("DISCORD_CHANNEL_WEBHOOK_URL")


weather_url = "https://opendata-download-metfcst.smhi.se/api/category/snow1g/version/1/geotype/point/lon/18.2282/lat/59.3086/data.json"


async def main(url: str = weather_url):
    weather = Weather(url)
    csv_data = await weather.get_weather()
    logger.info("fetching completed")

    if csv_data is None:
        logger.error("Failed to fetch weather data.")
        return

    advice = await get_clothing_advice(csv_data)
    logger.info(advice)

    await send_to_discord(discord_webhook_url, advice)


async def run_scheduler():
    start_scheduler()
    while True:
        await asyncio.sleep(3600)  # Keep the scheduler running


# if __name__ == "__main__":
#     asyncio.run(run_scheduler())


if __name__ == "__main__":
    asyncio.run(main())
