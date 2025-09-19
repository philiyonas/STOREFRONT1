import os
import django
import sys
sys.path.append(os.getcwd())
 

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from django.db import connection

TABLE = 'store_orderitem'
DUP_IDX = 'store_orderitem_order_id_acf8722d_fk_store_order_id'

with connection.cursor() as c:

    # check if the index exists
    c.execute(
        "SELECT COUNT(*) FROM information_schema.STATISTICS "
        "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s AND INDEX_NAME = %s",
        [TABLE, DUP_IDX]
    )
    exists = c.fetchone()[0] > 0

    if not exists:
        print(f"Index `{DUP_IDX}` not found on {TABLE}. Nothing to do.")
    else:
        # check whether a foreign key constraint references this index name
        c.execute(
            "SELECT COUNT(*) FROM information_schema.KEY_COLUMN_USAGE "
            "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s "
            "AND (CONSTRAINT_NAME = %s OR INDEX_NAME = %s) "
            "AND REFERENCED_TABLE_NAME IS NOT NULL",
            [TABLE, DUP_IDX, DUP_IDX]
        )
        fk_used = c.fetchone()[0] > 0

        if fk_used:
            print(f"Index `{DUP_IDX}` appears to be used by a FOREIGN KEY constraint. Do NOT drop it automatically.")
            print("Run `SHOW CREATE TABLE store_orderitem;` and paste the output here so I can provide exact safe ALTER statements.")
        else:
            print(f"Dropping index `{DUP_IDX}` on {TABLE}...")
            c.execute(f"ALTER TABLE `{TABLE}` DROP INDEX `{DUP_IDX}`;")
            print("Dropped. Re-run migrations now if needed.")