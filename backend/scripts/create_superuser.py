#!/usr/bin/env python
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
os.environ.setdefault("PYTHONPATH", "/app")

django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

USERNAME = "admin"
PASSWORD = "admin"
EMAIL = "admin@admin.com"

try:
    if not User.objects.filter(username=USERNAME).exists():
        User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
        print("✅ Superuser criado com sucesso!")
    else:
        print("ℹ️ Superuser já existe.")
except Exception as e:
    print(f"❌ Erro ao criar superuser: {e}")