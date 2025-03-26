#!/usr/bin/env bash

set -e
set -x


PYTHONPATH=$(pwd) poetry run pytest app/tests/api/routes/