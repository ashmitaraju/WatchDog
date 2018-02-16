import httplib, urllib, base64

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '863007e7f6dd4cfab18e3de9c8fb1fbd',
}


def verifyFace(faceIds, GROUP_ID):

    ids = str (faceIds)
   # print ids
    body = "{ 'personGroupId':'%s', 'faceIds': %s, 'maxNumOfCandidatesReturned':1, 'confidenceThreshold': 0.5 } " %(GROUP_ID, ids)

    #print body

    conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/identify" , body, headers)
    response = conn.getresponse()
    data = response.read()
    #print (data) + "hey"
    
    conn.close()
    return data