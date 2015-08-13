"""
Definition of models.
"""

from django.db import models
import azureImageProvider

class InputImages(models.Model):
    set_name = models.CharField(max_length=200)
    image_1 = models.ImageField()
    image_2 = models.ImageField()

    imageProvider = azureImageProvider.azureImageProvider()

    def image_1_url(self):
        strm = self.imageProvider.getUrl('myblob')
        return strm;

