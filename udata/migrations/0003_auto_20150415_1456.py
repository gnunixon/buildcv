# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('udata', '0002_langskill_human'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='awards',
            options={'ordering': ['-year']},
        ),
        migrations.AlterModelOptions(
            name='study',
            options={'ordering': ['-begin_year', '-end_year']},
        ),
        migrations.AlterModelOptions(
            name='work',
            options={'ordering': ['-begin_year', '-end_year']},
        ),
        migrations.AddField(
            model_name='human',
            name='user',
            field=models.OneToOneField(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
