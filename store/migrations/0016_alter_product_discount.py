# Generated by Django 4.1.7 on 2023-03-28 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0015_alter_product_discount_price_alter_product_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="discount",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
