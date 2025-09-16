"""Export audit CSVs:
- all_current_assignments.csv: all products that are not in 'Uncategorized'
- recent_updates.csv: products updated in the last N minutes (useful to identify recently applied changes)
"""
import os, sys, datetime
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront1.settings')
import django
django.setup()
from store.models import Product, Collection
import csv

OUT_DIR = os.path.join(os.getcwd(), 'scripts')
N_MINUTES = 60

uncoll = Collection.objects.filter(title__iexact='uncategorized').first()
uncoll_id = uncoll.pk if uncoll else None

# Export all non-uncategorized products
all_path = os.path.join(OUT_DIR, 'all_current_assignments.csv')
with open(all_path, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['product_id','title','collection_id','collection_title','last_update'])
    qs = Product.objects.exclude(collection=uncoll_id) if uncoll_id else Product.objects.all()
    for p in qs.iterator():
        w.writerow([p.pk, p.title, p.collection.pk if p.collection else '', p.collection.title if p.collection else '', p.last_update.isoformat() if p.last_update else ''])

# Export recent updates
recent_path = os.path.join(OUT_DIR, 'recent_updates.csv')
cutoff = datetime.datetime.utcnow() - datetime.timedelta(minutes=N_MINUTES)
# Django stores timezone-aware datetimes; for simplicity we'll compare naive UTC
with open(recent_path, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['product_id','title','collection_id','collection_title','last_update'])
    qs = Product.objects.filter(last_update__gte=cutoff)
    for p in qs.iterator():
        w.writerow([p.pk, p.title, p.collection.pk if p.collection else '', p.collection.title if p.collection else '', p.last_update.isoformat() if p.last_update else ''])

print('Wrote:', all_path, recent_path)
