# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('udata', '0018_auto_20150522_2202'),
    ]

    operations = [
        migrations.CreateModel(
            name='LangSkillValTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=128, null=True, blank=True)),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='udata.LangSkillVal', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'udata_langskillval_translation',
                'db_tablespace': '',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='langskillvaltranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AlterModelOptions(
            name='study',
            options={'ordering': ['-end_year', '-begin_year']},
        ),
        migrations.AlterModelOptions(
            name='work',
            options={'ordering': ['-end_year', '-begin_year']},
        ),
    ]
