# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPostModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('posted_at', models.DateField(auto_created=True)),
                ('edited_at', models.DateField(auto_now=True)),
                ('slug', models.SlugField()),
                ('content', models.TextField()),
                ('title', models.CharField(max_length=240)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
