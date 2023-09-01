#!/usr/bin/env bash
# exit on error
set -o errexit

poetry install
export PYTHON_VERSION="3.11.5"
python manage.py collectstatic --no-input
python manage.py migrate
