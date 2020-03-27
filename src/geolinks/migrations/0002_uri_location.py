# Generated by Django 3.0.4 on 2020-03-27 16:58

from django.db import migrations
import location_field.models.plain


class Migration(migrations.Migration):

    dependencies = [
        ('geolinks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uri',
            name='location',
            field=location_field.models.plain.PlainLocationField(blank=True, max_length=63, null=True),
        ),
    ]
