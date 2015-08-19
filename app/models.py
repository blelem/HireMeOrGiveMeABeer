﻿"""
Definition of models.
"""

from django.db import models
import azureImageProvider

class InputImages(models.Model):
    set_name = models.CharField(max_length=200)
    image_1 = models.ImageField()
    image_2 = models.ImageField()

    imageProvider = azureImageProvider.azureImageProvider()

    def image_url(self, subindex, thumbnail = False):
        """ Returns the url for one of the images of the set"""

        blobname = str(self.pk) + "-" + str(subindex)
        if (thumbnail):
            blobname += "-tn"
        blobname += ".jpg"
        online=  self.imageProvider.getUrl(blobname).replace(r"https://mansewiz.blob.core.windows.net/matchfeatures/", 
                                                            r"./static/app/img/")
        return online
       # return r"https://mansewiz.blob.core.windows.net/matchfeatures/1-0-tn.jpg"
       # return r"./static/app/img/1-0-tn.jpg"
        return self.imageProvider.getUrl(blobname)

