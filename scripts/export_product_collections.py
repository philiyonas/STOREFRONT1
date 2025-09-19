"""Export products and their collection assignments to CSV.

Usage:
  .\storevenv\Scripts\python.exe .\scripts\export_product_collections.py

Writes: scripts/output/product_collections.csv
"""
import os
import csv
import sys
import pathlib

repo_root = str(pathlib.Path(__file__).resolve().parents[1])
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront1.settings')
import django
django.setup()
from store.models import Product

out_dir = pathlib.Path(__file__).resolve().parents[0] / 'output'
out_dir.mkdir(exist_ok=True)
out_path = out_dir / 'product_collections.csv'

with out_path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['product_id', 'title', 'collection_id', 'collection_title', 'last_update', 'unit_price', 'inventory'])
    for p in Product.objects.select_related('collection').order_by('id'):
        cid = p.collection.pk if p.collection_id is not None else ''
        ctitle = p.collection.title if p.collection_id is not None else ''
        writer.writerow([p.pk, p.title, cid, ctitle, p.last_update.isoformat() if p.last_update else '', str(p.unit_price), p.inventory])

print(f"Wrote {out_path}")
