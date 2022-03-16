import logging, json, scipy
import azure.functions as func
import numpy as np
import pandas as pd

# from tensorflow.keras.applications.vgg16 import VGG16
# from tensorflow.keras.models import Model
from azure.storage.blob import BlobServiceClient, BlobClient, BlobLeaseClient
from io import BytesIO
from PIL import Image
from scipy.spatial import distance
from _business.images.images import fetch_images_from_url
from _business.utils.listToString import listToString
from _service.post.upload_stream import upload_to_blob_dtb

# These are the constants for blob storage
connect_str = 'DefaultEndpointsProtocol=https;AccountName=aiimage2;AccountKey=Zq+6nm/m9M5kX2iDxCmclL6080aJvklfbLTt2753bGvCQqj/Pgt0d4ypLeuaE2JWm9BxwMEv5oJ7+AStK58Bzw==;EndpointSuffix=core.windows.net'
Text = "Test.txt"
Base = "base-image"
Database = "database"
Links = "All_links.txt"
extension = ('.jpg', '.jpeg', '.png', '.svg','.JPG', '.JPEG', '.PNG', '.SVG')

# These are declarations for AI model
# vgg16 = VGG16(weights='imagenet',include_top=True,pooling='max',input_shape=(224,224,3))
# ICmodel = Model(inputs=vgg16.input,outputs=vgg16.get_layer('fc2').output)

# This is the get_images cloud function
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
# Detect the URL from the parameters at end of request (?url=[URL])
    websiteUrl = req.params.get('url')
    print('Detected URL:')
    print(websiteUrl)
    
# Run Process
    imagelist = fetch_images_from_url(websiteUrl, 'hello')
    # print(imagelist)
    image_line = listToString(imagelist)
    upload_to_blob_dtb(image_line.rstrip(','), connect_str,Database,Links)
    blist_service_client = BlobServiceClient.from_connection_string(connect_str)
    blist_client = blist_service_client.get_container_client(Base)
    blist_list = blist_client.list_blobs()
    
# Process first image in base-image
    for blist in blist_list:
        img_base = blist.name
        if img_base.endswith(extension):
            print('The base image we found is:', img_base)
            image1_client = BlobClient.from_connection_string(connect_str, Base, img_base)
            with BytesIO() as input_blob:
                image1_client.download_blob().download_to_stream(input_blob)
                img_bytes = Image.open(input_blob)
                resized_image1 = np.resize(img_bytes, 224*224*3)
                img1 = np.array(resized_image1)
                # v1 = ICmodel.predict(img1.reshape(1, 224, 224, 3))
            print(img1)
            
# Start loading information of database
    source2 = BlobClient.from_connection_string(connect_str, Database, Links)
    with BytesIO() as input_blob:
        source2.download_blob().download_to_stream(input_blob)
        input_blob.seek(0)
        df_blob = pd.read_csv(input_blob)
        data2 = df_blob.values
        lines = len(list(data2))
    for i in range(lines):
        link = str(data2[i])[2:-2]   
        blob_name = link.split("/")[-1]
        lease = BlobLeaseClient(source2)
        lease.acquire()
        source_props = source2.get_blob_properties()
        # print("Download state: " + source_props.lease.state)
        dest_blob = BlobClient.from_connection_string(connect_str,Database, str(blob_name))
        dest_blob.start_copy_from_url(link)
        # properties = dest_blob.get_blob_properties()
        # copy_props = properties.copy
        # print("Downloading: " + blob_name)
        if (source_props.lease.state == "leased"):
            lease.break_lease()                                  # Break the lease on the source blob.
            source_props = source2.get_blob_properties()         # Update the destination blob's properties to check the lease state.
            # print("Completed!")
        blist2_service_client = BlobServiceClient.from_connection_string(connect_str)
        blist2_client = blist2_service_client.get_container_client(Database)
        blist2_list = blist2_client.list_blobs()
        
# From list of images, stream each image and perform comparison
    for blist2 in blist2_list:
        img2_base = blist2.name
        if img2_base.endswith(extension):
            print('We found this from database:', img2_base)
            image2_client = BlobClient.from_connection_string(connect_str, Database, img2_base)
            with BytesIO() as input_blob2:
                image2_client.download_blob().download_to_stream(input_blob2)
                img2_bytes = Image.open(input_blob2)
                resized_image2 = np.resize(img2_bytes, 224*224*3)
                img2 = np.array(resized_image2)
                # v2 = ICmodel.predict(img2.reshape(1, 224, 224, 3))
                print(img2)                                    # Print all images in database from URL
                # c = str(round(scipy.spatial.distance.cosine(v1, v2), 2)*100)
                # print("The similarity percentage is: %s", str(c))
                
    headers = {"Access-Control-Allow-Origin": "*"}
    
    return func.HttpResponse(json.dumps({ "images": imagelist}), headers=headers)