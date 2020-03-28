# Generated by Django 3.0.4 on 2020-03-28 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('bot', '0002_auto_20200327_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='web_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.Group'),
        ),
    ]
