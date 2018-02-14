import httplib, urllib, base64


GROUP_ID = '02'
#PERSON_ID = '0fe14084-9aea-4724-86c4-366d093b2980'
#PATH_TO_IMAGE = '../images/bby.jpg'



headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '863007e7f6dd4cfab18e3de9c8fb1fbd',
}





def verifyFace(faceIds):

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