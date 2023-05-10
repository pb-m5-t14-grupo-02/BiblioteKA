#!/usr/bin/env bash
# exit on error
set -o errexit

pip install poetry
poetry install
python manage.py makemigrations
python manage.py migrate
python manage.py create_admin
python manage.py create_users 100
python manage.py create_books