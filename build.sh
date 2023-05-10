#!/usr/bin/env bash
# exit on error
set -o errexit

pip install poetry
poetry install
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py create_admin
python manage.py create_books