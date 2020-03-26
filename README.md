# Plataforma web-bot para makers

## Instalacion

Ejecuta `./manage.sh` y te creará el .virtualenv y más cosas.

Escribe un fichero environment con esto:
```
export SECRET_KEY='una_string_complicada'
export TELEGRAM_TOKEN="uid:hash_que_te_dice_botfather"
```

También puedes crear un archivo .env dentro de `src/` con esto:

```
SECRET_KEY='una_string_complicada'
TELEGRAM_TOKEN='uid:hash_que_te_dice_botfather'
```