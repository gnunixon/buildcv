# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('udata', '0010_human_lang'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbilityTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('comment', models.CharField(max_length=1024)),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='udata.Ability', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'udata_ability_translation',
                'db_tablespace': '',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AwardsTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='udata.Awards', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'udata_awards_translation',
                'db_tablespace': '',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StudyTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('faculty', models.CharField(max_length=255, null=True, blank=True)),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='udata.Study', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'udata_study_translation',
                'db_tablespace': '',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('function', models.CharField(max_length=255)),
                ('comments', models.CharField(max_length=255, null=True, blank=True)),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='udata.Work', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'udata_work_translation',
                'db_tablespace': '',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='worktranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AlterUniqueTogether(
            name='studytranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AlterUniqueTogether(
            name='awardstranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AlterUniqueTogether(
            name='abilitytranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.RemoveField(
            model_name='ability',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='ability',
            name='title',
        ),
        migrations.RemoveField(
            model_name='awards',
            name='description',
        ),
        migrations.RemoveField(
            model_name='awards',
            name='title',
        ),
        migrations.RemoveField(
            model_name='study',
            name='faculty',
        ),
        migrations.RemoveField(
            model_name='work',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='work',
            name='function',
        ),
    ]
