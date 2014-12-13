# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_tag_blogpost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='blogpost',
        ),
        migrations.AddField(
            model_name='blogpostmodel',
            name='tags',
            field=models.ManyToManyField(to='blog.Tag', blank=True),
            preserve_default=True,
        ),
    ]
