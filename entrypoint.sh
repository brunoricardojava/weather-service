#!/bin/sh

./manage.py migrate
poetry run task coverage

exec "$@"
