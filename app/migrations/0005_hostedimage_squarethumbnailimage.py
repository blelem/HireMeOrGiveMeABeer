# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import azure_storage.storage


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20150825_0817'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostedimage',
            name='squareThumbnailImage',
            field=models.ImageField(default=b'./default.jpg', storage=azure_storage.storage.AzureStorage(), upload_to=b''),
        ),
    ]
