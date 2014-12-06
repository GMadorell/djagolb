# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20141206_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpostmodel',
            name='md_content',
            field=models.TextField(default=b'', editable=False),
            preserve_default=True,
        ),
    ]
