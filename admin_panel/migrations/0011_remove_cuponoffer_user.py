# Generated by Django 3.2 on 2021-05-29 04:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0010_alter_cuponoffer_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuponoffer',
            name='user',
        ),
    ]