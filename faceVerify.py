import httplib
import urllib
import json
import yaml
import requests

with open("config.yaml", "r") as f:
    config = yaml.load(f)


def face_verify(face_ids, group_id):
    headers = {
        'Ocp-Apim-Subscription-Key': config['azure']['faceAPIkey'],
    }

    ids = str(face_ids)
    data = { 
        'personGroupId': group_id,
        'face_ids': ids, 
        'maxNumOfCandidatesReturned':1,
        'confidenceThreshold': 0.5 ,
    } 
    base_url = "https://westcentralus.api.cognitive.microsoft.com"
    endpoint = "/face/v1.0/identify"
    response = requests.post( base_url + endpoint, headers = headers, data = data)
    return response.json()


def get_face(face):

    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': config['azure']['faceAPIkey'],
    }

    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false'  
    }
    
    data = face 

    base_url = "https://westcentralus.api.cognitive.microsoft.com"
    endpoint = "/face/v1.0/detect"

    response = requests.post( base_url + endpoint, params = params, headers = headers, data = data )

    return response.json()
