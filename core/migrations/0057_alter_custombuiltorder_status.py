# Generated by Django 5.1.6 on 2025-05-03 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0056_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custombuiltorder',
            name='status',
            field=models.CharField(choices=[('15', '15 minuets'), ('12', '12 minuets'), ('9', '9 minuets'), ('6', '6 minuets'), ('3', '3 minuets'), ('03', '3 Hur'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='03', max_length=20),
        ),
    ]
