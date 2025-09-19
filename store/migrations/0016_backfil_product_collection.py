from django.db import migrations

def forwards(apps, schema_editor):
    Collection = apps.get_model('store', 'Collection')
    Product = apps.get_model('store', 'Product')

    unc, _ = Collection.objects.get_or_create(title='Uncategorized')
    # use collection_id to update in bulk
    Product.objects.filter(collection__isnull=True).update(collection_id=unc.pk)

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_make_product_collection_nullable'),  # REPLACE to point to the file created above
    ]

    operations = [
        migrations.RunPython(forwards, reverse_code=migrations.RunPython.noop),
    ]