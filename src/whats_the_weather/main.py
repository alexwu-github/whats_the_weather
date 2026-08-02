import httpx
import asyncio
from dataclasses import dataclass
from pprint import pprint
import csv
from whats_the_weather.getWeather import Weather

##https://ai.google.dev/gemini-api/docs/get-started

url = "https://opendata-download-metfcst.smhi.se/api/category/snow1g/version/1/geotype/point/lon/18.2282/lat/59.3086/data.json"

def main(url: str):
    weather = Weather(url)
    asyncio.run(weather.fetch_weather())
    print('fetching completed')

main(url)