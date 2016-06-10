# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ability',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('comment', models.CharField(max_length=1024)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Awards',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('year', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CV',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('public', models.BooleanField()),
                ('pdf', models.FileField(null=True, upload_to=b'cvs', blank=True)),
                ('abilities', models.ManyToManyField(to='udata.Ability')),
                ('awards', models.ManyToManyField(to='udata.Awards')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CVTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('text', models.TextField()),
                ('image', models.ImageField(upload_to=b'cv_thumbs')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Human',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('birthday', models.DateField()),
                ('phone', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=75)),
                ('web', models.CharField(max_length=1024)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LangSkill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LangSkillVal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Study',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inst', models.CharField(max_length=255)),
                ('faculty', models.CharField(max_length=255)),
                ('begin_year', models.IntegerField()),
                ('end_year', models.IntegerField()),
                ('human', models.ForeignKey(to='udata.Human')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inst', models.CharField(max_length=255)),
                ('function', models.CharField(max_length=255)),
                ('comments', models.CharField(max_length=255)),
                ('begin_year', models.IntegerField()),
                ('end_year', models.IntegerField()),
                ('human', models.ForeignKey(to='udata.Human')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='langskill',
            name='language',
            field=models.ForeignKey(to='udata.Language'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='langskill',
            name='read',
            field=models.ForeignKey(related_name='read_skill', to='udata.LangSkillVal'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='langskill',
            name='speak',
            field=models.ForeignKey(related_name='speak_skill', to='udata.LangSkillVal'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='langskill',
            name='write',
            field=models.ForeignKey(related_name='write_skill', to='udata.LangSkillVal'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cv',
            name='human',
            field=models.ForeignKey(to='udata.Human'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cv',
            name='studies',
            field=models.ManyToManyField(to='udata.Study'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cv',
            name='template',
            field=models.ForeignKey(to='udata.CVTemplate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cv',
            name='works',
            field=models.ManyToManyField(to='udata.Work'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='awards',
            name='human',
            field=models.ForeignKey(to='udata.Human'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ability',
            name='human',
            field=models.ForeignKey(to='udata.Human'),
            preserve_default=True,
        ),
    ]
