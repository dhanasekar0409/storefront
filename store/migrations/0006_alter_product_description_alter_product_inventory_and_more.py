# Generated by Django 5.0.7 on 2024-07-14 02:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0005_alter_collection_options_alter_customer_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="inventory",
            field=models.IntegerField(
                validators=[django.core.validators.MinValueValidator(1)]
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="promotions",
            field=models.ManyToManyField(blank=True, to="store.promotion"),
        ),
        migrations.AlterField(
            model_name="product",
            name="unit_price",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=6,
                validators=[django.core.validators.MinValueValidator(1)],
            ),
        ),
    ]
