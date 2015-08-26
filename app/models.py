"""
Definition of models.
"""

import StringIO
import os
import binascii
from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
import azureImageProvider
from azure_storage.storage import AzureStorage
from PIL import Image

azureStorage = AzureStorage()


# TODO: Remove this class, shouldn't be used anymore with the new model structure.
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
        return self.imageProvider.getUrl(blobname)

    

class ImageSet(models.Model):
    ''' Many images organized in a set (Many-to-One)'''

    user = models.CharField(max_length=30) # This is a placeholder, until a proper user model exists.


class HostedImageManager(models.Manager):
    def create_HostedImage(self, fullResImage, imageSet):
       ''' Randomize the name of the image, create a thumbnail '''
       
       #Randomize the name
       randomString = binascii.b2a_hex(os.urandom(15))
       os.path.splitext("path_to_file")[0]
       oldName = fullResImage.name 
       extension = os.path.splitext(oldName)[1]
       newName = randomString + extension     
       fullResImage.name = newName

       #Create the thumbnail.
       size = 256, 256

       thumb = Image.open(fullResImage)
       thumb.thumbnail(size, Image.ANTIALIAS)   
       thumb_io = StringIO.StringIO()
       thumb.save(thumb_io, format='JPEG')
       thumb_file = InMemoryUploadedFile(thumb_io, None, randomString + '-tn' + '.jpg', 'image/jpeg',
                                  thumb_io.len, None)
       
       #Create the model entry
       hostedImage = self.create(fullResImage= fullResImage, 
                             thumbnailImage = thumb_file,
                             imageSet = imageSet)

       return hostedImage

class HostedImage(models.Model):
    ''' Images hosted on an Azure blob'''

    fullResImage = models.ImageField(storage = azureStorage, default = "./default.jpg")
    thumbnailImage = models.ImageField(storage = azureStorage, default = "./default.jpg")
    imageSet = models.ForeignKey(ImageSet)
    objects = HostedImageManager()

    

        