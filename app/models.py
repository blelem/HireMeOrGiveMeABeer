"""
Definition of models.
"""

from django.db import models

class InputImages(models.Model):
    set_name = models.CharField(max_length=200)
    image_1 = models.ImageField()
    image_2 = models.ImageField()

    def image_1_url(self):
        # Accessing directly the Azure blob storage. TODO: access via a model.
        from azure.storage import BlobService
        blob_service = BlobService(account_name='mansewiz', account_key='nexzj9VdFGQeTwagdnLOrGp4nXWNuNnnCJkFJbpqT58/A5iX0kdEqcUF0AGvxj9h0s7DXJdZruQGUj9KVldCpQ==')
        strm = blob_service.make_blob_url('matchfeatures','myblob')
        return strm;

