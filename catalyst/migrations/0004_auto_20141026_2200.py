# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalyst', '0003_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='latitude',
            field=models.DecimalField(default=0.0, max_digits=11, decimal_places=8),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='longitude',
            field=models.DecimalField(default=0.0, max_digits=11, decimal_places=8),
            preserve_default=True,
        ),
    ]
