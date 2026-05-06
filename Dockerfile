FROM python:3.12-slim

WORKDIR /app

RUN pip install uv --no-cache-dir

COPY pyproject.toml .
RUN uv sync --no-dev --no-cache

COPY . .

RUN chmod +x /app/entrypoint.sh

ENV FLASK_ENV=production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uv", "run", "gunicorn", "wsgi:app", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "60"]
