# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import azure_storage.storage


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_inputimages_image_2'),
    ]

    operations = [
        migrations.CreateModel(
            name='HostedImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fullResImage', models.ImageField(storage=azure_storage.storage.AzureStorage(), upload_to=b'')),
            ],
        ),
        migrations.CreateModel(
            name='ImageSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='hostedimage',
            name='imageSet',
            field=models.ForeignKey(to='app.ImageSet'),
        ),
    ]
