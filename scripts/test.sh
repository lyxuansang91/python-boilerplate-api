#!/usr/bin/env bash

set -e
set +x

# Load environment variables từ file .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

POSTGRES_SERVER=${POSTGRES_SERVER:-"localhost"}
POSTGRES_PORT=${POSTGRES_PORT:-"5432"}
POSTGRES_USER=${POSTGRES_USER:-"postgres"}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-""}
POSTGRES_DB_TEST=${POSTGRES_DB_TEST:-"stockbot_test"}

export PGPASSWORD=$POSTGRES_PASSWORD

if ! psql -U "$POSTGRES_USER" -h "$POSTGRES_SERVER" -p "$POSTGRES_PORT" -lqt | cut -d \| -f 1 | grep -qw "$POSTGRES_DB_TEST"; then
    echo "Database $POSTGRES_DB_TEST does not exist. Creating a new one..."
    createdb -U "$POSTGRES_USER" -h "$POSTGRES_SERVER" -p "$POSTGRES_PORT" "$POSTGRES_DB_TEST"
else
    echo "Database $POSTGRES_DB_TEST already exists."
fi

# ENVIRONMENT=test poetry run alembic upgrade head

# Add -s after pytest to display the logs of test cases.
ENVIRONMENT=test poetry run pytest app/tests/api/routes/test_register
ENVIRONMENT=test poetry run pytest app/tests/api/routes/healths
ENVIRONMENT=test poetry run pytest app/tests/api/routes/auth
ENVIRONMENT=test poetry run pytest -s app/tests/api/routes/users
