# Generated by Django 3.0.4 on 2020-03-28 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geolinks', '0003_auto_20200327_1724'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uri',
            name='permanent',
        ),
        migrations.RemoveField(
            model_name='uri',
            name='validated',
        ),
    ]