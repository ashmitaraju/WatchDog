import requests
import yaml

with open("config.yaml", "r") as f:
    config = yaml.load(f)

    
def get_objects(image):

    #print config['azure']['cvAPIkey']
    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': config['azure']['cvAPIkey'],
    }

    params = {
        'visualFeatures' : 'Categories, Tags'
    }

    data = image

    base_url = 'https://westcentralus.api.cognitive.microsoft.com/vision'
    api_endpoint = '/v1.0/analyze'

    response = requests.post(base_url + api_endpoint, headers = headers, params = params, data = data)
    #print response.json()
    return response.json()

