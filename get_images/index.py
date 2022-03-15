import logging
import azure.functions as func
import json

from _business.images.images import fetch_images_from_url
from _business.utils.listToString import listToString
# from tensorflow.keras.applications.vgg16 import VGG16
# from tensorflow.keras.models import Model

# These are the constants for blob storage
connect_str = 'DefaultEndpointsProtocol=https;AccountName=aiimage2;AccountKey=Zq+6nm/m9M5kX2iDxCmclL6080aJvklfbLTt2753bGvCQqj/Pgt0d4ypLeuaE2JWm9BxwMEv5oJ7+AStK58Bzw==;EndpointSuffix=core.windows.net'
Text = "Test.txt"
Base = "base-image"
Database = "database"
Links = "All_links.txt"

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
    images = fetch_images_from_url(websiteUrl, 'hello')
    print(images)
    
    headers = {"Access-Control-Allow-Origin": "*"}
    return func.HttpResponse(json.dumps({ "images": images}), headers=headers)
