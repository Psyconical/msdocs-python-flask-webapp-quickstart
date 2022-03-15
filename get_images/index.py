import logging

import azure.functions as func
import json

from _business.images.images import fetch_images_from_url
from _business.utils.listToString import listToString

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
