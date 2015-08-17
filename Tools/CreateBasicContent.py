from azure.storage import BlobService
import json
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("importRules", help="A json file defining the images to upload to the azure blob service")
args = parser.parse_args()

#Connect to the azure blob service
blob_service = BlobService(account_name='mansewiz', account_key='nexzj9VdFGQeTwagdnLOrGp4nXWNuNnnCJkFJbpqT58/A5iX0kdEqcUF0AGvxj9h0s7DXJdZruQGUj9KVldCpQ==')
container_name = 'matchfeatures';    

with open(args.importRules, 'r') as infile:
    images = json.load(infile)

basepath = os.path.dirname(args.importRules)
os.chdir(basepath) 

for image in images:    
    idx = 0;
    for filename in image['files']:
         #First upload the full res images
        name = str(image['pk']) + "-" + str( idx) + ".jpg"
        print "Uploading " + filename + " to " + name
        blob_service.put_block_blob_from_path(
           container_name,
           name,
           filename,
           x_ms_blob_content_type='image/jpg' )
        idx += 1


