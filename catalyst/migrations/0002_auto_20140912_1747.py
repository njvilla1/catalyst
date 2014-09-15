# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalyst', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='pic_url',
        ),
        migrations.AddField(
            model_name='profile',
            name='photo',
            field=models.ImageField(null=True, upload_to=b'catalyst/profile_photos'),
            preserve_default=True,
        ),
    ]
