import asyncio
from whats_the_weather.getWeather import Weather
from whats_the_weather.get_clothing_advice import get_clothing_advice

##https://ai.google.dev/gemini-api/docs/get-started

url = "https://opendata-download-metfcst.smhi.se/api/category/snow1g/version/1/geotype/point/lon/18.2282/lat/59.3086/data.json"
weather_csv_path = "src/whats_the_weather/weather.csv"

async def main(url: str):
    weather = Weather(url)
    await weather.get_weather()
    print('fetching completed')

    with open(weather_csv_path, "r") as f:
        csv_data = f.read()

    advice = get_clothing_advice(csv_data)
    print(advice)

if __name__ == "__main__":
    asyncio.run(main(url))