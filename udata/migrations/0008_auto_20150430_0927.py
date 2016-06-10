# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('udata', '0007_tmpcv'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tmpcv',
            name='abilities',
        ),
        migrations.RemoveField(
            model_name='tmpcv',
            name='awards',
        ),
        migrations.RemoveField(
            model_name='tmpcv',
            name='human',
        ),
        migrations.RemoveField(
            model_name='tmpcv',
            name='studies',
        ),
        migrations.RemoveField(
            model_name='tmpcv',
            name='template',
        ),
        migrations.RemoveField(
            model_name='tmpcv',
            name='works',
        ),
        migrations.DeleteModel(
            name='TmpCV',
        ),
    ]
