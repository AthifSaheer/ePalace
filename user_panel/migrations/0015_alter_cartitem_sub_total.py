# Generated by Django 3.2 on 2021-05-11 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_panel', '0014_auto_20210511_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='sub_total',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
