#!/bin/sh
set -e

mkdir -p /app/instance
uv run flask --app wsgi db upgrade
exec uv run flask --app wsgi run --host=0.0.0.0 --port=8000 --debug
