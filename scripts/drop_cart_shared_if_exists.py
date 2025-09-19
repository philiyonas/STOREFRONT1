r"""Drop the cart_shared column if it exists. Safe one-off script to reconcile DB schema.

Usage:
  .\storevenv\Scripts\python.exe .\scripts\drop_cart_shared_if_exists.py

Back up the DB before running in production.
"""

import os
import sys
import django
import pathlib


def main():
    # Ensure repo root is on sys.path so we can import the project package.
    repo_root = str(pathlib.Path(__file__).resolve().parents[1])
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)
    print(f"cwd={os.getcwd()}, repo_root={repo_root}")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront1.settings')
    django.setup()
    from django.db import connection

    TABLE = 'store_cart'
    COL = 'cart_shared'

    with connection.cursor() as cursor:
        # Check existence
        cursor.execute(
            "SELECT COUNT(*) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME=%s AND COLUMN_NAME=%s",
            [TABLE, COL],
        )
        row = cursor.fetchone()
        if not row:
            print(f"Could not determine column existence for {TABLE}.{COL}. Aborting.")
            return
        exists = bool(row[0])
        if not exists:
            print(f"Column {COL} does not exist on {TABLE}. Nothing to do.")
            return

        print(f"Dropping column {COL} from {TABLE}...")
        try:
            # Use a direct ALTER TABLE DROP; database user must have ALTER/DDL privileges.
            cursor.execute(f"ALTER TABLE `{TABLE}` DROP COLUMN `{COL}`;")
        except Exception as exc:
            print("Error while dropping column:", exc)
            raise
        else:
            print("Dropped.")


if __name__ == '__main__':
    main()
