# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20141213_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='blogpost',
            field=models.ManyToManyField(to='blog.BlogPostModel', blank=True),
            preserve_default=True,
        ),
    ]
