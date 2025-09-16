import os
import sys
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE','storefront1.settings')
import django
django.setup()
from django.db import connection
cur = connection.cursor()
cur.execute("SELECT COLUMN_NAME, DATA_TYPE FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='store_orderitem'")
cols = cur.fetchall()
print('orderitem columns:', cols)
from store.models import OrderItem
print('model fields:', [(f.name,f.column) for f in OrderItem._meta.fields])
