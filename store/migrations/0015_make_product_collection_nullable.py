from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_remove_cart_cart_shared_remove_product_collection_and_more'),  # REPLACE with your latest migration
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='collection',
            field=models.ForeignKey(
                to='store.Collection',
                on_delete=django.db.models.deletion.PROTECT,
                related_name='products',
                null=True,
                blank=True,
            ),
        ),
    ]