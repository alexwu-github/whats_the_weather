fix:
	poetry run ruff check --fix .
	poetry run ruff format .

run:
	poetry run python -m src/whats_the_weather/main.py
