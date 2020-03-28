#!/bin/sh
set -e
DIR=$(dirname $0)
test "$DIR" && cd "$DIR"
. .virtualenv/bin/activate
git pull
./manage.py check
./manage.py clearsessions
./manage.py collectstatic --no-input
./manage.py migrate
