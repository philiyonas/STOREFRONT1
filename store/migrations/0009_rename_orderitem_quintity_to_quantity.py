# Generated migration to rename OrderItem.quintity -> quantity
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_remove_collection_product_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='quintity',
            new_name='quantity',
        ),
    ]
