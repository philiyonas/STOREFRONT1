"""Auto-classify uncategorized products using simple keyword heuristics.

Usage:
  python scripts/auto_classify.py         # dry-run (shows suggested assignments)
  python scripts/auto_classify.py --apply # apply suggested assignments to DB

The script looks for products whose collection is NULL or whose collection title is 'Uncategorized',
then tries to match keywords in the product title or description to a collection.  It prints a
summary and a small sample of suggested assignments.

This is intentionally conservative — run without --apply first to inspect suggestions.
"""
import os
import sys
import argparse

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront1.settings')

import django
django.setup()

from store.models import Product, Collection

# Simple keyword -> collection name mapping.
# You can extend this list as needed.
KEYWORD_MAP = [
    (['baking', 'flour', 'yeast', 'sugar', 'cake', 'cookie'], 'Baking'),
    (['spice', 'spices', 'cumin', 'pepper', 'paprika', 'allspice'], 'Spices'),
    (['pet', 'dog', 'cat', 'fish', 'bird'], 'Pets'),
    (['magazine', 'magazines'], 'Magazines'),
    (['flower', 'flowers', 'bouquet'], 'Flowers'),
    (['clean', 'detergent', 'soap', 'bleach'], 'Cleaning'),
    (['beauty', 'shampoo', 'soap', 'lotion', 'skincare'], 'Beauty'),
    (['toy', 'lego', 'doll', 'games'], 'Toys'),
    (['stationary', 'stationery', 'notebook', 'pen', 'paper'], 'Stationary'),
    (['veg', 'vegetable', 'vegitables', 'produce'], 'Vegitables'),
    (['grocery', 'bread', 'milk', 'eggs', 'grocery'], 'Grocery'),
    (['appetizer', 'snack', 'chips', 'roll'], 'Grocery'),
]


def normalize_text(s):
    return (s or '').lower()


def build_collection_lookup():
    # map normalized collection title -> Collection instance
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
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true', help='Apply suggested assignments')
    args = parser.parse_args()

    collection_lookup = build_collection_lookup()

    # Find targets: either collection is null or title == Uncategorized (case-insensitive)
    unc_candidates = Product.objects.filter(collection__isnull=True) | Product.objects.filter(collection__title__iexact='uncategorized')
    unc_candidates = unc_candidates.distinct()

    total = unc_candidates.count()
    print(f'Found {total} uncategorized products to analyze')

    suggestions = []
    for p in unc_candidates.iterator():
        coll, kw = suggest_assignment_for_product(p, collection_lookup)
        if coll:
            suggestions.append((p.pk, p.title, coll.pk, coll.title, kw))

    print(f'Found {len(suggestions)} suggested assignments')

    # Show top 20 suggestions
    for s in suggestions[:20]:
        pid, title, cid, cname, kw = s
        print(f'P#{pid}: "{title}" -> {cname} (matched "{kw}")')

    # Summarize by collection
    from collections import Counter
    ccounts = Counter([s[3] for s in suggestions])
    if ccounts:
        print('\nSummary of suggestions:')
        for cname, cnt in ccounts.most_common():
            print(f'  {cname}: {cnt}')

    if not suggestions:
        print('\nNo suggestions found with current heuristics.')
        return

    if args.apply:
        print('\nApplying suggestions...')
        applied = 0
        for pid, title, cid, cname, kw in suggestions:
            Product.objects.filter(id=pid).update(collection=cid)
            applied += 1
        print(f'Applied assignments for {applied} products')
    else:
        print('\nDry-run: no changes applied. Rerun with --apply to perform updates.')


if __name__ == '__main__':
    main()
