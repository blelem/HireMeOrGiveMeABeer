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
from PIL import Image, ImageOps

azureStorage = AzureStorage()

class ImageSet(models.Model):
    ''' Many images organized in a set (Many-to-One)'''

    user = models.CharField(max_length=30) # This is a placeholder, until a proper user model exists.


class HostedImageManager(models.Manager):
    def create_HostedImage(self, fullResImage, imageSet):
       ''' Randomize the name of the image, create thumbnails '''
       
       #Randomize the name
       randomString = binascii.b2a_hex(os.urandom(15))
       os.path.splitext("path_to_file")[0]
       oldName = fullResImage.name 
       extension = os.path.splitext(oldName)[1]
       newName = randomString + extension     
       fullResImage.name = newName


       size = 256, 256
       original_image = Image.open(fullResImage)

       #Create a thumbnail, respecting the aspect ratio.
       thumb = original_image.copy()
       thumb.thumbnail(size, Image.ANTIALIAS)   
       thumb_io = StringIO.StringIO()
       thumb.save(thumb_io, format='JPEG')
       thumb_file = InMemoryUploadedFile(thumb_io, None, randomString + '-tn' + '.jpg', 'image/jpeg',
                                  thumb_io.len, None)
       
       #Create a square thumbnail
       square = ImageOps.fit(original_image, size)
       square_io = StringIO.StringIO()
       square.save(square_io, format='JPEG')
       square_file = InMemoryUploadedFile(square_io, None, randomString + '-tn-sq' + '.jpg', 'image/jpeg',
                                  square_io.len, None)

       #Create the model entry
       hostedImage = self.create(fullResImage= fullResImage, 
                             thumbnailImage = thumb_file,
                             squareThumbnailImage = square_file,
                             imageSet = imageSet)

       return hostedImage

class HostedImage(models.Model):
    ''' Images hosted on an Azure blob'''

    fullResImage = models.ImageField(storage = azureStorage, default = "./default.jpg")
    thumbnailImage = models.ImageField(storage = azureStorage, default = "./default.jpg")
    squareThumbnailImage = models.ImageField(storage = azureStorage, default = "./default.jpg")
    imageSet = models.ForeignKey(ImageSet)
    objects = HostedImageManager()

    

        