# What's the Weather

Fetches an hourly weather forecast from [SMHI](https://opendata.smhi.se/) for a given location, saves it to CSV with timestamps converted to Swedish local time, asks Gemini to turn it into a short Swedish-language clothing recommendation for the day, and posts the result to a Discord channel via webhook.

## How it works

1. `Weather.get_weather()` in [getWeather.py](src/whats_the_weather/getWeather.py) requests the forecast from SMHI's point-forecast API and writes it to `src/whats_the_weather/weather.csv`, converting each timestamp from UTC to `Europe/Stockholm` time and adding a calculated `feels_like` temperature (wind chill, via [calculate_feels_like_temp.py](src/whats_the_weather/calculate_feels_like_temp.py)).
2. [main.py](src/whats_the_weather/main.py) reads that CSV and passes it to `get_clothing_advice()` in [get_clothing_advice.py](src/whats_the_weather/get_clothing_advice.py), which prompts Gemini for a Swedish summary of the day's weather and what to wear (layers, umbrella, sunglasses, winter jacket, windproof jacket, etc. depending on conditions).
3. `send_to_discord()` in [discord_notification.py](src/whats_the_weather/discord_notification.py) posts a message to a Discord channel through a webhook.

## Requirements

- Python >= 3.14
- [Poetry](https://python-poetry.org/) for dependency management
- A Gemini API key (get one at [ai.google.dev](https://ai.google.dev/gemini-api/docs/get-started))
- A Discord webhook URL (Server Settings → Integrations → Webhooks in the channel you want to post to)

## Setup

```bash
poetry install
```

Create a `.env` file in the project root with your Gemini API key and Discord webhook URL:

```
GEMINI_API_KEY=your-key-here
DISCORD_CHANNEL_WEBHOOK_URL=your-discord-webhook-url-here
```

## Usage

```bash
poetry run python src/whats_the_weather/main.py
```

This fetches the current forecast, writes `weather.csv`, prints a Swedish clothing recommendation based on the day's temperature, wind, precipitation, and sun/snow conditions, and posts it to Discord.

### Changing the location

The forecast location is set by the `url` variable at the top of [main.py](src/whats_the_weather/main.py), which encodes a longitude/latitude pair in the SMHI API path:

```
.../geotype/point/lon/<longitude>/lat/<latitude>/data.json
```

Swap in your own coordinates to get a forecast for a different location.

## Project structure

```
src/whats_the_weather/
├── main.py                      # entry point: fetch weather, get advice, notify Discord
├── getWeather.py                # SMHI fetch + CSV export
├── calculate_feels_like_temp.py # wind chill calculation
├── get_clothing_advice.py       # Gemini-based advice generation
├── discord_notification.py      # Discord webhook notification
└── weather.csv                  # generated forecast data (overwritten each run)
```
