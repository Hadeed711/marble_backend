#!/usr/bin/env python
import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sundar_marbles.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='products_product';")
    columns = [row[0] for row in cursor.fetchall()]
    print("Columns in products_product table:")
    for col in sorted(columns):
        print(f"  - {col}")
