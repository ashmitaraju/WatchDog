import httplib, urllib, base64



headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '863007e7f6dd4cfab18e3de9c8fb1fbd',
}


def trainFaces ( GROUP_ID ):
    personGroupId = GROUP_ID

    body = ""

    print body

    conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/persongroups/%s/train" %personGroupId, body, headers)
    response = conn.getresponse()
    data = response.read()
    
    print "person id = " + data
    conn.close()
    return response.status