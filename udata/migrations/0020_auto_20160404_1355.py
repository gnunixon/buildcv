# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('udata', '0019_auto_20150522_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='human',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
