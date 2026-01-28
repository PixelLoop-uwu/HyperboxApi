FROM astral-sh/uv:python3.11-alpine

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-cache

COPY . .

EXPOSE 8000

CMD ["uv run uvicorn main:api --host 0.0.0.0 --port 8000"]