# Generated by Django 3.0.4 on 2020-03-28 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geolinks', '0004_auto_20200328_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uri',
            name='url',
            field=models.URLField(unique=True),
        ),
    ]