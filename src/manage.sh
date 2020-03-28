#!/bin/sh

PYTHON=python3
PIPARGS="-i https://pypi.org/simple"
MAKEMIGRATIONS=0
COLLECTSTATIC=1
SAFETY=0

log () {
    echo ----------------------------------------------------------------------
    echo $*
}

# para evitar el "cd" cuando estamos en un chroot y ejecutamos en una linea
dir=$(dirname $0)
test "$dir" && cd "$dir"

set -e

test $PYTHON = python2 -a ! -e /usr/bin/virtualenv && {
    if test -e /usr/bin/apt-get; then 
        apt-get install -y virtualenv python-virtualenv
    else
        pip install virtualenv
    fi
}

test $PYTHON = python3 -a ! -e /usr/bin/pyvenv && {
    if test -e /usr/bin/apt-get; then 
        apt-get install -y python3-venv
    fi
}

test -e .virtualenv || {
    log creando .virtualenv
	if test $PYTHON = python2; then
		virtualenv .virtualenv --python=$PYTHON
	else
		$PYTHON -m venv .virtualenv
	fi
}

log Activando virtualenv
. .virtualenv/bin/activate

log Instalando .virtualenv
pip install -r requirements.txt $PIPARGS

if test "$SAFETY" -ne 0; then
    log "Safety check (un mes)"
    pip install safety
    pip freeze | safety check --bare
fi

# hasta no meter las migraciones en el repo
if test "$MAKEMIGRATIONS" -ne 0; then
    for MODEL in */models.py; do
        APP=$(echo $MODEL | sed 's/\/.*//')
        test -d $APP/migrations/ && continue
        log Creando migraciones aplicacion $APP
        ./manage.py makemigrations $APP
    done

    log Creando migraciones extra
    ./manage.py makemigrations
fi

log Aplicando migraciones
./manage.py migrate

if test -e /usr/bin/sqlite3; then
    SUPERUSERS=$(echo "select count() from auth_user where is_superuser and is_active" | ./manage.py dbshell)
    test $SUPERUSERS = 0 && {
        log Creando superusuario
        ./manage.py createsuperuser --username admin --email root@galotecnia.com --noinput
    }
fi

if test "$COLLECTSTATIC" -ne 0; then
    log ./manage.py collectstatic
    ./manage.py collectstatic --noinput
fi

log ./manage.py check
./manage.py check

log ./manage.py $*
./manage.py $*
