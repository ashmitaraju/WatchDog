import json
import httplib, urllib, base64
headers = {
      # Request headers
      'Content-Type': 'application/octet-stream',
      'Ocp-Apim-Subscription-Key': 'fc32fc93924140508f44d7cd1c4e2a90',
  }
def getPerson(img):

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
  if data["faces"]:
    print data["faces"]
  return data