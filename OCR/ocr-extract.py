from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import json
import sys
import time

def azure_get_data():
    subscription_key = "ACCESS KEY"
    endpoint = "ENDPOINT URL"
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    #remote_image_url = "https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/master/articles/cognitive-services/Computer-vision/Images/readsample.jpg"
    
    # Provide the image path
    local_image_handwritten_path = "sample4.jpg"
    local_image_handwritten = open(local_image_handwritten_path, "rb")
    recognize_handwriting_results = computervision_client.read_in_stream(local_image_handwritten, raw=True)
    operation_location_remote = recognize_handwriting_results.headers["Operation-Location"]
    # Get Operation ID
    operation_id = operation_location_remote.split("/")[-1]

    # Repeat if Operation ID result status is 'notStarted' or 'running'
    while True:
        get_handw_text_results = computervision_client.get_read_result(operation_id)
        if get_handw_text_results.status not in ['notStarted', 'running']:
            break
        time.sleep(1)
    

    # Print the detected text, line by line
    if get_handw_text_results.status == OperationStatusCodes.succeeded:
        print(type(get_handw_text_results.analyze_result.read_results))
        for text_result in get_handw_text_results.analyze_result.read_results:
            for line in text_result.lines:
                print(line.text)
                

if __name__ == '__main__':
    azure_get_data()