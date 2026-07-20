#!/bin/bash
set -e

# Применяем миграции
python manage.py migrate


# Собираем статику
python manage.py collectstatic --noinput

# Запускаем Gunicorn с оптимальными параметрами
exec gunicorn \
    config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --threads 2 \
    --timeout 120