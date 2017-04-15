# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-05 13:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'cities',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.URLField()),
                ('datetime', models.DateTimeField()),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('details', models.TextField()),
                ('register_link', models.URLField(blank=True, null=True)),
                ('sharing_text', models.CharField(blank=True, max_length=140, null=True)),
                ('has_interactions', models.BooleanField(default=False)),
                ('interaction_text', models.CharField(blank=True, max_length=200, null=True)),
                ('interaction_confirmation_text', models.CharField(blank=True, max_length=200, null=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('is_upcoming', models.BooleanField(default=True)),
                ('is_interaction_active', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('city', models.ManyToManyField(to='events.City')),
            ],
            options={
                'ordering': ['-datetime'],
                'verbose_name_plural': 'events',
            },
        ),
        migrations.CreateModel(
            name='Interaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100)),
                ('votes', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
            ],
            options={
                'ordering': ['-pk'],
                'verbose_name': 'interaction item',
                'verbose_name_plural': 'interaction items',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('latitude', models.CharField(max_length=11)),
                ('longitude', models.CharField(max_length=11)),
            ],
            options={
                'verbose_name_plural': 'locations',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.Location'),
        ),
    ]
