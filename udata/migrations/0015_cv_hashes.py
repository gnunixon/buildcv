# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('udata', '0014_auto_20150513_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='cv',
            name='hashes',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
