from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_backfil_product_collection'),  # REPLACE to point to the data-migration above
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='collection',
            field=models.ForeignKey(
                to='store.Collection',
                on_delete=django.db.models.deletion.PROTECT,
                related_name='products',
                null=False,
                blank=False,
            ),
        ),
    ]