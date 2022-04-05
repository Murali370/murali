import json
import io
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image, ImageDraw, ImageFont
import sys
import time

'''
Authenticate
Authenticates your credentials and creates a client.
'''
credential = json.load(open('credential.json'))
API_KEY = credential['API_KEY']
ENDPOINT = credential['ENDPOINT']

computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))
image_url = 'https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/master/articles/cognitive-services/Computer-vision/Images/readsample.jpg'
local_file = './images/1.jpg'
response = computervision_client.read(url=image_url,language='en',raw=True)
response = computervision_client.read_in_stream(open(local_file, 'rb'), language='en', raw=True)
operationLocation = response.headers['Operation-Location']
operation_id = operationLocation.split('/')[-1]
time.sleep(5)
result = computervision_client.get_read_result(operation_id)
 
print(result)
print(result.status)
print(result.analyze_result)

if result.status == OperationStatusCodes.succeeded:
    read_results = result.analyze_result.read_results
    for analyzed_result in read_results:
        for line in analyzed_result.lines:
            print(line.text)

image = Image.open(local_file)
if result.status == OperationStatusCodes.succeeded:
    read_results = result.analyze_result.read_results
    for analyzed_result in read_results:
        for line in analyzed_result.lines:
            x1, y1, x2, y2, x3, y3, x4, y4 = line.bounding_box
            draw = ImageDraw.Draw(image)
            draw.line(
                ((x1, y1), (x2, y1), (x2, y2), (x3, y2), (x3, y3), (x4, y3), (x4, y4), (x1, y4), (x1, y1)),
                fill=(255, 0, 0),
                width=5
            )
image.show()
image.save('hand writing result.jpg')