# Generated by Django 5.0.3 on 2024-05-03 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_profile_profile_picture_alter_profile_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user_type',
            field=models.CharField(choices=[('host', 'Host'), ('guest', 'Guest')], default='guest', max_length=10),
        ),
    ]
