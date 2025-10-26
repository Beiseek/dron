#!/usr/bin/env python
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dron_site.settings')
django.setup()

from django.core.management import execute_from_command_line

if __name__ == '__main__':
    print("Создание миграций...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    
    print("Применение миграций...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("Готово!")