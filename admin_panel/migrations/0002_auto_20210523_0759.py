# Generated by Django 3.2 on 2021-05-23 02:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_panel', '0025_alter_product_offer_price'),
        ('admin_panel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_for', models.CharField(default='Today special offer', max_length=20)),
                ('offer_percentage', models.PositiveIntegerField()),
                ('time_period', models.DateTimeField()),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_panel.category')),
            ],
        ),
        migrations.CreateModel(
            name='CuponOrReferralOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_for', models.CharField(default='Today special offer', max_length=20)),
                ('cupon_code', models.CharField(max_length=15)),
                ('offer_percentage', models.PositiveIntegerField()),
                ('time_period', models.DateTimeField()),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_for', models.CharField(default='Today special offer', max_length=20)),
                ('offer_percentage', models.PositiveIntegerField()),
                ('time_period', models.DateTimeField()),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_panel.product')),
            ],
        ),
        migrations.RemoveField(
            model_name='category_offer',
            name='category',
        ),
        migrations.DeleteModel(
            name='Cupon_or_Referral_Offer',
        ),
        migrations.RemoveField(
            model_name='product_offer',
            name='product',
        ),
        migrations.DeleteModel(
            name='Category_Offer',
        ),
        migrations.DeleteModel(
            name='Product_Offer',
        ),
    ]