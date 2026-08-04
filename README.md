# What's the Weather

Fetches an hourly weather forecast from [SMHI](https://opendata.smhi.se/) for a given location, converts it to CSV with timestamps in Swedish local time, asks Gemini to turn it into a short Swedish-language clothing recommendation for the day, and posts the result to a Discord channel via webhook.

## How it works

1. `Weather.get_weather()` in [get_weather.py](src/whats_the_weather/get_weather.py) requests the forecast from SMHI's point-forecast API and builds a CSV in memory (via `io.StringIO`), converting each timestamp from UTC to `Europe/Stockholm` time and adding a calculated `feels_like` temperature (wind chill, via [calculate_feels_like_temp.py](src/whats_the_weather/calculate_feels_like_temp.py)). It returns the CSV as a string — nothing is written to disk.
2. [main.py](src/whats_the_weather/main.py) passes that string to `get_clothing_advice()` in [get_clothing_advice.py](src/whats_the_weather/get_clothing_advice.py), which prompts Gemini for a Swedish summary of the day's weather and what to wear (layers, umbrella, sunglasses, winter jacket and boots, depending on conditions). The response is bullet-pointed, uses Celsius and 24-hour times, ignores hours before 07:00, and includes precipitation probability when rain or snow is likely. Errors from the Gemini API (bad request, server error, empty response) are caught and re-raised as a `RuntimeError`.
3. `send_to_discord()` in [discord_notification.py](src/whats_the_weather/discord_notification.py) posts the advice to a Discord channel through a webhook.

## Requirements

- Python >= 3.14
- [Poetry](https://python-poetry.org/) for dependency management
- A Gemini API key (get one at [aistudio.google.com/apikey](https://aistudio.google.com/apikey))
- A Discord webhook URL (Server Settings → Integrations → Webhooks in the channel you want to post to)

## Setup

Install Poetry itself with [pipx](https://pipx.pypa.io/) — this is the recommended way, since pipx keeps Poetry in its own isolated environment instead of mixing it into a project or system Python:

```bash
pipx install poetry
```

Then install the project's dependencies:

```bash
poetry install
```

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your-key-here
DISCORD_CHANNEL_WEBHOOK_URL=your-discord-webhook-url-here
LOG_LEVEL=INFO
```

`LOG_LEVEL` is optional and defaults to `INFO`.

## Usage

```bash
poetry run python -m whats_the_weather.main
```

This fetches the current forecast, logs a Swedish clothing recommendation based on the day's temperature, wind, precipitation, and sun/snow conditions, and posts it to Discord.

The project must be run as a module (`-m`), not by file path — the package is declared as `{include = "whats_the_weather", from = "src"}`, so running `python src/whats_the_weather/main.py` puts the wrong directory on `sys.path` and the package imports fail.

`poetry run` is what guarantees the virtualenv's interpreter is used. If you'd rather type plain `python`, activate the environment first with `source $(poetry env info --path)/bin/activate`, or select the Poetry interpreter in VS Code so new terminals activate it automatically.

### Scheduled runs

[scheduler.py](src/whats_the_weather/scheduler.py) sets up an APScheduler cron job that runs the whole flow daily at 07:00 `Europe/Stockholm`. It is not active by default — [main.py](src/whats_the_weather/main.py) currently runs `main()` once and exits. To run on a schedule instead, swap the entry point to `run_scheduler()`:

```python
if __name__ == "__main__":
    asyncio.run(run_scheduler())
```

### Changing the location

The forecast location is set by the `weather_url` variable in [main.py](src/whats_the_weather/main.py), which encodes a longitude/latitude pair in the SMHI API path:

```
.../geotype/point/lon/<longitude>/lat/<latitude>/data.json
```

Swap in your own coordinates to get a forecast for a different location.

### Changing the AI rules

The whole prompt is one f-string — the `contents` argument in [get_clothing_advice.py:20-38](src/whats_the_weather/get_clothing_advice.py#L20-L38). Edit it directly; there's no config file.

- **Language:** change `- Svara på svenska` on [line 30](src/whats_the_weather/get_clothing_advice.py#L30).
- **Format and length:** the rules on [lines 23-31](src/whats_the_weather/get_clothing_advice.py#L23-L31).
- **Clothing advice:** one condition per line on [lines 34-37](src/whats_the_weather/get_clothing_advice.py#L34-L37).
- **Model:** `model=` on [line 19](src/whats_the_weather/get_clothing_advice.py#L19).

Keep `{csv_data}` on [line 21](src/whats_the_weather/get_clothing_advice.py#L21) — that's what feeds the forecast in.

## Docker

```bash
docker build -t whats-the-weather .
docker run --env-file .env whats-the-weather
```

The [Dockerfile](Dockerfile) uses a two-stage build: dependencies are installed into an in-project `.venv` in the builder stage, then copied into a slim runtime image that runs `python -m whats_the_weather.main`.

## Development

```bash
make fix
```

Runs `ruff check --fix` and `ruff format` across the project. See [Makefile](Makefile).

## Project structure

```
src/whats_the_weather/
├── main.py                      # entry point: fetch weather, get advice, notify Discord
├── get_weather.py               # SMHI fetch + in-memory CSV conversion
├── calculate_feels_like_temp.py # wind chill calculation
├── get_clothing_advice.py       # Gemini-based advice generation
├── discord_notification.py      # Discord webhook notification
├── scheduler.py                 # APScheduler daily 07:00 cron job
└── notebook.ipynb               # scratch notebook for exploring the SMHI data
```
