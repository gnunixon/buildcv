# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('udata', '0009_auto_20150430_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='human',
            name='lang',
            field=models.CharField(default=b'ro', max_length=8, null=True, blank=True),
            preserve_default=True,
        ),
    ]
