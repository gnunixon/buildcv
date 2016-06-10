# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('udata', '0003_auto_20150415_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='awards',
            name='description',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cv',
            name='abilities',
            field=models.ManyToManyField(to='udata.Ability', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cv',
            name='awards',
            field=models.ManyToManyField(to='udata.Awards', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='work',
            name='comments',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='work',
            name='end_year',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
