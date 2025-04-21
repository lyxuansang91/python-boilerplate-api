#!/bin/bash
export POSTGRES_DB=stockbot_test
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload --app-dir app
