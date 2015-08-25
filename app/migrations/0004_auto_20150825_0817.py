# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import azure_storage.storage


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20150824_2107'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostedimage',
            name='thumbnailImage',
            field=models.ImageField(default=b'./default.jpg', storage=azure_storage.storage.AzureStorage(), upload_to=b''),
        ),
        migrations.AlterField(
            model_name='hostedimage',
            name='fullResImage',
            field=models.ImageField(default=b'./default.jpg', storage=azure_storage.storage.AzureStorage(), upload_to=b''),
        ),
    ]
