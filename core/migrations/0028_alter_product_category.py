# Generated by Django 5.1.6 on 2025-04-10 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_carousal_alter_userorder_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('RAM', 'PC RAM'), ('GPC', 'GRAPHICS CARDS'), ('AIC', 'AIR COOLER'), ('HHD', 'HARD DRIVE'), ('PWS', 'POWER SUPPLY'), ('SSD', 'SSD'), ('LIQ', 'LIQUID COOLER'), ('PRS', 'PROCESSOR')], max_length=50),
        ),
    ]
