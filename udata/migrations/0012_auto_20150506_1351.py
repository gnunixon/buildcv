# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('udata', '0011_auto_20150504_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cv',
            name='public',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
