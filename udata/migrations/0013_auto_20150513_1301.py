# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('udata', '0012_auto_20150506_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='begin_year',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
