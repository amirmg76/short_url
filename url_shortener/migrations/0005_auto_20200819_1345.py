# Generated by Django 3.0.5 on 2020-08-19 13:45

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('url_shortener', '0004_auto_20200819_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='ip_views',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.jsonb.JSONField(), default=list, size=None),
        ),
    ]