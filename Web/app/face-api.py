
import httplib, urllib, base64, json
headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '863007e7f6dd4cfab18e3de9c8fb1fbd',
}

#params = urllib.urlencode({ 'personGroupId' : GROUP_ID
#})

def addFace ( GROUP_ID, PERSON_ID, PATH_TO_IMAGE):
    personGroupId = GROUP_ID
    personId = PERSON_ID

    body = "{ 'url' : '%s' }" %PATH_TO_IMAGE

    #print body
    print PATH_TO_IMAGE
    conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/persongroups/%s/persons/%s/persistedFaces" %(personGroupId, personId) , body, headers)
    response = conn.getresponse()
    data = response.read()
    print (data)
    conn.close()
    return json.loads (data)


def addPerson ( GROUP_ID, PERSON_NAME, PERSON_DATA ):
    params = urllib.urlencode({ 'personGroupId' : GROUP_ID
    })

    personGroupId = GROUP_ID

    body = "{ 'name': '%s', 'userData': '%s' }" %( PERSON_NAME , PERSON_DATA)

    print body

    conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/persongroups/%s/persons" %personGroupId, body, headers)
    response = conn.getresponse()
    data = response.read()
    print "person id = " + data
    conn.close()
    return data

    
def createGroup ( GROUP_ID, PERSON_NAME, PERSON_DATA):
    personGroupId = GROUP_ID

    body = "{ 'name': '%s', 'userData': '%s' }" %( PERSON_NAME , PERSON_DATA)

    print body

    conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("PUT", "/face/v1.0/persongroups/%s" %personGroupId, body, headers)
    response = conn.getresponse()
    data = response.read()
    print "person id = " + data
    conn.close()
    return response.status


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