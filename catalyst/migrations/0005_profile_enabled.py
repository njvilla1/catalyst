# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalyst', '0004_auto_20141026_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='enabled',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
