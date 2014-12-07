# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20141206_2323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpostmodel',
            name='id',
        ),
        migrations.AlterField(
            model_name='blogpostmodel',
            name='slug',
            field=models.SlugField(serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
