# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-11 16:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_code', models.CharField(max_length=200, unique=True)),
                ('type', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name_plural': 'devices',
            },
        ),
    ]
