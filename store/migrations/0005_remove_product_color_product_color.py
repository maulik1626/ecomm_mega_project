# Generated by Django 4.1.7 on 2023-03-27 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0004_productsize_sized_products_remove_product_size_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="product", name="color",),
        migrations.AddField(
            model_name="product",
            name="color",
            field=models.ManyToManyField(
                blank=True, related_name="products", to="store.productcolor"
            ),
        ),
    ]
