import os, sys
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE','storefront1.settings')
import django
django.setup()
from django.db import connection
cur=connection.cursor()
cur.execute("SELECT CONSTRAINT_NAME, TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME FROM information_schema.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA=DATABASE() AND REFERENCED_TABLE_NAME='store_product' AND REFERENCED_COLUMN_NAME='id'")
for row in cur.fetchall():
    print(row)
