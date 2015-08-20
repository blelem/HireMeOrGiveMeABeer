from azure.storage import BlobService

class azureImageProvider:
    def __init__(self):
         # TODO: This secret key should NEVER be left unencrypted like this.
        self.blob_service = BlobService(account_name='mansewiz', account_key='nexzj9VdFGQeTwagdnLOrGp4nXWNuNnnCJkFJbpqT58/A5iX0kdEqcUF0AGvxj9h0s7DXJdZruQGUj9KVldCpQ==')
        self.container_name = 'matchfeatures';    


    def getUrl(self, blobname):
        return self.blob_service.make_blob_url(self.container_name,blobname)