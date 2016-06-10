# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('udata', '0004_auto_20150424_0822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='human',
            name='birthday',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='human',
            name='web',
            field=models.CharField(max_length=1024, null=True, blank=True),
            preserve_default=True,
        ),
    ]
