#!/bin/bash
set -e

# --- Переменные ---
PROJECT_NAME="dron"
GIT_REPO="https://github.com/Beiseek/dron.git"
PROJECT_DIR="/var/www/dron-site"
VENV_DIR="$PROJECT_DIR/venv"
USER=$(whoami) # Используем текущего пользователя

echo "--- 1. Обновление системы и установка зависимостей ---"
sudo apt-get update
sudo apt-get install -y python3-venv python3-pip nginx git

echo "--- 2. Настройка брандмауэра ---"
sudo ufw allow 'Nginx Full'
sudo ufw allow 'OpenSSH'
sudo ufw --force enable

echo "--- 3. Клонирование репозитория из GitHub ---"
sudo mkdir -p $PROJECT_DIR
sudo chown -R $USER:$USER $PROJECT_DIR
git clone $GIT_REPO $PROJECT_DIR

cd $PROJECT_DIR

echo "--- 4. Создание виртуального окружения и установка зависимостей Python ---"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

echo "--- 5. Настройка Django ---"
# Создание .env файла для секретных данных
echo "SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')" > .env
echo "DEBUG=False" >> .env
echo "ALLOWED_HOSTS=ktlab.store,91.229.9.60" >> .env

# Применение миграций и сбор статики
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

echo "--- 6. Тестовый запуск Gunicorn ---"
# Это нужно для проверки, что приложение запускается
# Вы можете прервать его после проверки (Ctrl+C)
echo "Сейчас будет тестовый запуск. Если ошибок нет, остановите его (Ctrl+C) и продолжайте по инструкции."
gunicorn --bind 0.0.0.0:8000 dron_site.wsgi

echo "--- Установка завершена! ---"
echo "Далее настройте Gunicorn и Nginx, используя файлы gunicorn.service и nginx.conf."
