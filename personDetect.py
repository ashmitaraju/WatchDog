import json
import httplib
import urllib


headers = {
      # Request headers
      'Content-Type': 'application/octet-stream',
      'Ocp-Apim-Subscription-Key': 'fc32fc93924140508f44d7cd1c4e2a90',
  }


def get_person(img):

    params = urllib.urlencode({'visualFeatures': 'Faces, Categories, Tags'})

    # personGroupId = GROUP_ID
    body = img

    # print body
    conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    # print "person id = " + data
    conn.close()
    data = json.loads(data)
    if data["faces"]:
        print data["faces"]
    return data
