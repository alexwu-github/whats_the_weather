FROM python:3.14.6-slim AS builder

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create true \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-root --no-interaction --no-ansi --only main



FROM python:3.14.6-slim AS runner

WORKDIR /app

COPY --from=builder /app/.venv ./.venv
COPY src/ ./src/

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src"

EXPOSE 8000

CMD ["python", "-m", "whats_the_weather.main"]