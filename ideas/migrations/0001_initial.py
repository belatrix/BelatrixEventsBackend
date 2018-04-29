# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-04-29 05:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
            ],
        ),
        migrations.CreateModel(
            name='IdeaParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ideas.Idea')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'team member',
                'verbose_name_plural': 'groups',
            },
        ),
        migrations.CreateModel(
            name='IdeaScores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Idea score',
                'verbose_name_plural': 'Idea scores',
            },
        ),
        migrations.CreateModel(
            name='IdeaScoresCriteria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('weight', models.PositiveIntegerField(default=1)),
            ],
            options={
                'verbose_name': 'Score category',
                'verbose_name_plural': 'Score categories',
            },
        ),
        migrations.CreateModel(
            name='IdeaVotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
                ('idea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ideas.Idea')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'votes',
            },
        ),
        migrations.AddField(
            model_name='ideascores',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ideas.IdeaScoresCriteria'),
        ),
        migrations.AddField(
            model_name='ideascores',
            name='idea',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ideas.Idea'),
        ),
        migrations.AddField(
            model_name='ideascores',
            name='jury',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='ideavotes',
            unique_together=set([('idea', 'participant')]),
        ),
        migrations.AlterUniqueTogether(
            name='ideascores',
            unique_together=set([('idea', 'jury', 'category')]),
        ),
        migrations.AlterUniqueTogether(
            name='ideaparticipant',
            unique_together=set([('idea', 'user')]),
        ),
    ]
