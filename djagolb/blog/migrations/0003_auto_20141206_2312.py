# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20141206_2040'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogpostmodel',
            old_name='content',
            new_name='html_content',
        ),
        migrations.AddField(
            model_name='blogpostmodel',
            name='md_content',
            field=models.TextField(default='a'),
            preserve_default=False,
        ),
    ]
