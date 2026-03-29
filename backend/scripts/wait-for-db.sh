#!/bin/sh

echo "=== Iniciando container Django ==="

echo "Aguardando banco de dados em $DB_HOST:$DB_PORT..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done
echo "Banco de dados pronto!"

echo "Aplicando migrations..."
python manage.py migrate --noinput

echo "Criando superusuário..."
python /app/scripts/create_superuser.py

echo "Iniciando servidor..."
exec python manage.py runserver 0.0.0.0:8000