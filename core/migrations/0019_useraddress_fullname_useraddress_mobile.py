# Generated by Django 5.1.6 on 2025-03-26 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_useraddress_addresstype_alter_useraddress_pin'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddress',
            name='fullName',
            field=models.CharField(default='Name', max_length=30),
        ),
        migrations.AddField(
            model_name='useraddress',
            name='mobile',
            field=models.CharField(default=0, max_length=10),
        ),
    ]
