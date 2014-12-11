# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpostmodel',
            name='posted_at',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
    ]
