# Generated by Django 5.0.3 on 2024-05-03 22:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_property'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='amenities',
        ),
    ]
