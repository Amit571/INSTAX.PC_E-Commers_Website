# Generated by Django 5.1.6 on 2025-05-03 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0061_alter_months_spacial_news_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='productImages',
            field=models.ImageField(blank=True, null=True, upload_to='product_images'),
        ),
        migrations.AlterField(
            model_name='product',
            name='productImages1',
            field=models.ImageField(blank=True, null=True, upload_to='product_images'),
        ),
        migrations.AlterField(
            model_name='product',
            name='productImages2',
            field=models.ImageField(blank=True, null=True, upload_to='product_images'),
        ),
        migrations.AlterField(
            model_name='product',
            name='productImages3',
            field=models.ImageField(blank=True, null=True, upload_to='product_images'),
        ),
    ]
