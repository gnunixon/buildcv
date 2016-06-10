# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('udata', '0016_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='parent',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='send',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
