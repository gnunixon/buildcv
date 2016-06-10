# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('udata', '0017_auto_20150521_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='study',
            name='end_year',
            field=models.IntegerField(default=65535),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='work',
            name='end_year',
            field=models.IntegerField(default=65535),
            preserve_default=True,
        ),
    ]
