# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('udata', '0006_auto_20150429_1333'),
    ]

    operations = [
        migrations.CreateModel(
            name='TmpCV',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('public', models.BooleanField()),
                ('pdf', models.FileField(null=True, upload_to=b'cvs', blank=True)),
                ('abilities', models.ManyToManyField(to='udata.Ability', null=True, blank=True)),
                ('awards', models.ManyToManyField(to='udata.Awards', null=True, blank=True)),
                ('human', models.ForeignKey(to='udata.Human')),
                ('studies', models.ManyToManyField(to='udata.Study')),
                ('template', models.ForeignKey(to='udata.CVTemplate')),
                ('works', models.ManyToManyField(to='udata.Work')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
