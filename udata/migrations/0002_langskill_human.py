# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('udata', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='langskill',
            name='human',
            field=models.ForeignKey(default=1, to='udata.Human'),
            preserve_default=False,
        ),
    ]
