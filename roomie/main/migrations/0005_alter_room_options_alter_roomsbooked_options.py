# Generated by Django 4.2.2 on 2023-08-30 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_roomsbooked_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='roomsbooked',
            options={'managed': False},
        ),
    ]
