# Generated by Django 4.1.7 on 2023-03-28 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0017_remove_product_size_product_size"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="sku",
            field=models.CharField(
                blank=True, editable=False, max_length=100, null=True
            ),
        ),
    ]