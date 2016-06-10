# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('udata', '0015_cv_hashes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('to_reload', models.CharField(max_length=255, null=True, blank=True)),
                ('success', models.BooleanField(default=True)),
                ('human', models.ForeignKey(to='udata.Human')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
