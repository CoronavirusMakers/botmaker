# Plataforma web-bot para makers

## Instalación

### BOT

Hablate con @botfather y crea un nuevo bot, dale nombre, y guarda la HTTP API key en el fichero `.env` de esta forma:

```
TELEGRAM_TOKEN = "uid:hash_que_te_dice_botfather"
```

### Django

Ejecuta `./manage.sh` y te creará el `.virtualenv` y más cosas.

Ejecuta `./manage.sh changepassword admin` para definir la contraseña del usuario `admin`.

Ejecuta `./manage.sh pycountry_import` para rellenar la base de datos de paises.

Escribe en el fichero `.env` lo siguiente:
```
SECRET_KEY = 'una_string_complicada'
```

## Ejecución

Para cargar el virtualenv ejecuta `. .virtualenv/bin/activate`

Para el django ejecuta `./manage.py runserver`

Para el bot ejecuta `./manage.py bot`

Visita http://localhost:8000/admin/
