# Generated by Django 3.2 on 2021-05-23 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_panel', '0025_alter_product_offer_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='offer_price',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]