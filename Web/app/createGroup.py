import httplib, urllib, base64

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '863007e7f6dd4cfab18e3de9c8fb1fbd',
}


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

