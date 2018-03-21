import httplib, urllib, base64, json, yaml

with open("config.yaml", "r") as f:
    config = yaml.load(f)




def verifyFace(faceIds, GROUP_ID):
    headers = {
    # Request headers
    #'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': config['azure']['faceAPIkey'],
    }

    #print "hi"
    ids = str (faceIds)
    #print ids
    body = "{ 'personGroupId':'%s', 'faceIds': %s, 'maxNumOfCandidatesReturned':1, 'confidenceThreshold': 0.5 } " %(GROUP_ID, ids)

    #print body

    conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/identify" , body, headers)
    response = conn.getresponse()
    data = response.read()
    #print data 
    data = json.loads (data)
    conn.close()
    return data

def getPerson(img):
    headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': config['azure']['cvAPIkey'],
    }
   # print config['azure']['faceAPIkey']
    params = urllib.urlencode({ 'visualFeatures' : 'Faces, Categories, Tags'})

    #personGroupId = GROUP_ID

    body = img #"{ 'url' : 'https://scontent-bom1-1.xx.fbcdn.net/v/t1.0-9/13346946_517091465156156_1729756543918513740_n.jpg?oh=fbc2f2fa04a9975444a0c92c287fda35&oe=5B121780' }"

    # print body

    conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v1.0/analyze?%s" %params, body, headers)
    response = conn.getresponse()
    data = response.read()
    # print "person id = " + data
    conn.close()
    data = json.loads(data)
    print data
   # if data["faces"]:
        #print data["faces"]
    return data


def getFace(face):
    headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': config['azure']['faceAPIkey'],
    }

   # config['azure']['faceAPIkey']

    params = urllib.urlencode({
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    })
    body = face

    try:
        # Execute the REST API call and get the response.
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()

        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        # print ("Response:")
        #print (json.dumps(parsed, sort_keys=True, indent=2))
        conn.close()

        return parsed

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
