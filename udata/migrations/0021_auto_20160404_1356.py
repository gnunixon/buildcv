# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('udata', '0020_auto_20160404_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worktranslation',
            name='comments',
            field=models.CharField(max_length=2048, null=True, blank=True),
        ),
    ]
