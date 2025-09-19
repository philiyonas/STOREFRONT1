# scripts/show_indexes.py
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()
from django.db import connection
with connection.cursor() as c:
    c.execute("SHOW INDEX FROM store_orderitem;")
    for row in c.fetchall():
        print(row) 