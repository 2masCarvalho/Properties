# Generated by Django 5.0.3 on 2024-05-05 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_alter_propertyimage_uploaded_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='location',
            field=models.CharField(choices=[('faro', 'Faro'), ('lagos', 'Lagos'), ('portimao', 'Portimão'), ('albufeira', 'Albufeira'), ('tavira', 'Tavira'), ('olhao', 'Olhão'), ('silves', 'Silves'), ('loule', 'Loulé'), ('vila_real_de_santo_antonio', 'Vila Real de Santo António')], max_length=100),
        ),
    ]
