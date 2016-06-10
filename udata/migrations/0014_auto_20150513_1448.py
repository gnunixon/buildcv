# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('udata', '0013_auto_20150513_1301'),
    ]

    operations = [
        migrations.CreateModel(
            name='CVTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pdf', models.CharField(max_length=255, null=True, blank=True)),
                ('png', models.CharField(max_length=255, null=True, blank=True)),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='udata.CV', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'udata_cv_translation',
                'db_tablespace': '',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='cvtranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.RemoveField(
            model_name='cv',
            name='pdf',
        ),
    ]
