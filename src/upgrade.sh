#!/bin/sh
set -e
. .virtualenv/bin/activate
git pull
./manage.py check
./manage.py clearsessions
./manage.py collectstatic --no-input
./manage.py migrate
