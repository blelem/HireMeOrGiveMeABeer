"""
Definition of models.
"""

from django.db import models
import azureImageProvider
from azure_storage.storage import AzureStorage

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



class HostedImage(models.Model):
    ''' A table of the images hosted on Azure blob'''

    # Table entries
    fullResImage = models.ImageField(storage=azureStorage)
   # thumbnailImage = models.ImageField()
    imageSet = models.ForeignKey(ImageSet);

