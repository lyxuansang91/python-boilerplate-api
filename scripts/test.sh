#!/usr/bin/env bash

set -e
set -x


PYTHONPATH=$(pwd) poetry run pytest -s app/tests/api/routes/test_register
PYTHONPATH=$(pwd) poetry run pytest -s app/tests/api/routes/healths
