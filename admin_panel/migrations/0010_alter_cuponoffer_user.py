# Generated by Django 3.2 on 2021-05-29 04:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('admin_panel', '0009_auto_20210529_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuponoffer',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]