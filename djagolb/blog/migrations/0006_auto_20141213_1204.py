# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20141213_1157'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='summary',
            new_name='summary_markdown',
        ),
        migrations.AddField(
            model_name='author',
            name='summary_html',
            field=models.TextField(default=b'', editable=False),
            preserve_default=True,
        ),
    ]
