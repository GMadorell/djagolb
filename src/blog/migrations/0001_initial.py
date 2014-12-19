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
                ('posted_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(serialize=False, primary_key=True)),
                ('md_content', models.TextField()),
                ('html_content', models.TextField(default=b'', editable=False)),
                ('title', models.CharField(max_length=240)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
