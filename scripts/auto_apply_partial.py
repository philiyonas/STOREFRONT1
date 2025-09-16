"""Apply auto-classification suggestions selectively.

This script recomputes suggestions using the same heuristics as auto_classify.py,
selects target collections whose suggestion counts are >= MIN_COUNT (default 20),
and applies assignments only for suggestions targeting those collections.

It prints a summary and sample applied items.
"""
import os
import sys
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront1.settings')
import django
django.setup()
from store.models import Product, Collection
from collections import Counter

MIN_COUNT = 20

# Reuse the same keyword mapping as auto_classify
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
    print('Total uncategorized products scanned:', unc_candidates.count())
    print('Total suggestions:', len(suggestions))
    print('Suggestion counts by collection:')
    for cname, cnt in ccounts.most_common():
        print(f'  {cname}: {cnt}')

    # pick collections meeting threshold
    chosen = {cname for cname,cnt in ccounts.items() if cnt >= MIN_COUNT}
    if not chosen:
        print(f'No collection meets threshold >= {MIN_COUNT}. Nothing applied.')
        return

    print(f'Collections selected for apply (count >= {MIN_COUNT}): {chosen}')

    # apply suggestions only for chosen collections
    to_apply = [s for s in suggestions if s[3] in chosen]
    print('Will apply for', len(to_apply), 'products')

    applied = 0
    samples = []
    for pid, title, cid, cname, kw in to_apply:
        Product.objects.filter(pk=pid).update(collection=cid)
        applied += 1
        if len(samples) < 20:
            samples.append((pid, title, cname, kw))

    print('Applied:', applied)
    print('\nSample applied:')
    for s in samples:
        print('P#{}: "{}" -> {} (matched "{}")'.format(*s))

if __name__ == '__main__':
    main()
