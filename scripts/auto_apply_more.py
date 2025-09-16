"""More-aggressive auto-apply: broader keywords and lower threshold.

This script applies suggestions where collection suggestion counts >= MIN_COUNT (default 5).
It writes a small audit CSV of applied changes to `scripts/classify_audit.csv`.
"""
import os
import sys
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront1.settings')
import django
django.setup()
from store.models import Product, Collection
from collections import Counter
import csv

MIN_COUNT = 5

# Broadened keyword map (added synonyms, removed overly-generic 'pen')
KEYWORD_MAP = [
    (['baking', 'flour', 'yeast', 'sugar', 'cake', 'cookie', 'bread', 'biscuit'], 'Baking'),
    (['spice', 'spices', 'cumin', 'pepper', 'paprika', 'allspice', 'seasoning'], 'Spices'),
    (['pet', 'dog', 'cat', 'fish', 'bird', 'lumpfish', 'crawfish'], 'Pets'),
    (['magazine', 'magazines'], 'Magazines'),
    (['flower', 'flowers', 'bouquet', 'potmum', 'palm'], 'Flowers'),
    (['clean', 'detergent', 'soap', 'bleach', 'hand soap', 'lime away', 'cleaner'], 'Cleaning'),
    (['beauty', 'shampoo', 'lotion', 'skincare', 'soap'], 'Beauty'),
    (['toy', 'lego', 'doll', 'games'], 'Toys'),
    (['stationary', 'stationery', 'notebook', 'paper'], 'Stationary'),
    (['veg', 'vegetable', 'vegitables', 'produce', 'salad'], 'Vegitables'),
    (['grocery', 'milk', 'eggs', 'grocery', 'appetizer', 'snack', 'chips', 'roll'], 'Grocery'),
]


def normalize_text(s):
    return (s or '').lower()


def build_collection_lookup():
    cols = {}
    for c in Collection.objects.all():
        cols[c.title.strip().lower()] = c
    return cols


def suggest_assignment_for_product(p, collection_lookup):
    text = normalize_text(p.title) + '\n' + normalize_text(p.description)
    for keywords, coll_name in KEYWORD_MAP:
        for kw in keywords:
            if kw in text:
                coll = collection_lookup.get(coll_name.lower())
                if coll:
                    return coll, kw
    return None, None


def main():
    collection_lookup = build_collection_lookup()
    unc_candidates = Product.objects.filter(collection__isnull=True) | Product.objects.filter(collection__title__iexact='uncategorized')
    unc_candidates = unc_candidates.distinct()

    suggestions = []
    for p in unc_candidates.iterator():
        coll, kw = suggest_assignment_for_product(p, collection_lookup)
        if coll:
            suggestions.append((p.pk, p.title, coll.pk, coll.title, kw))

    ccounts = Counter([s[3] for s in suggestions])
    print('found suggestions:', len(suggestions))
    print('counts by collection:')
    for cname,cnt in ccounts.most_common():
        print(' ', cname, cnt)

    chosen = {cname for cname,cnt in ccounts.items() if cnt >= MIN_COUNT}
    print('chosen for apply (>=', MIN_COUNT, '):', chosen)

    to_apply = [s for s in suggestions if s[3] in chosen]
    print('will apply for', len(to_apply), 'products')

    # Apply and write audit rows
    audit_path = os.path.join(os.getcwd(), 'scripts', 'classify_audit.csv')
    with open(audit_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['product_id','title','applied_collection_id','applied_collection_title','matched_kw'])
        applied = 0
        for pid, title, cid, cname, kw in to_apply:
            Product.objects.filter(pk=pid).update(collection=cid)
            writer.writerow([pid, title, cid, cname, kw])
            applied += 1

    print('applied', applied, 'and wrote audit to', audit_path)

if __name__ == '__main__':
    main()
