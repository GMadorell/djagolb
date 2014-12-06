# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20141206_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpostmodel',
            name='html_content',
            field=models.TextField(default=b'', editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogpostmodel',
            name='md_content',
            field=models.TextField(),
            preserve_default=True,
        ),
    ]
