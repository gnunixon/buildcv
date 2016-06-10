# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('udata', '0008_auto_20150430_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='langskill',
            name='language',
            field=models.CharField(max_length=128),
            preserve_default=True,
        ),
    ]
