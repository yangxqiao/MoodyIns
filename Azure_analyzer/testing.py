########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'abf4a7db13074ff096c50d114d629cf2',
}

params = urllib.parse.urlencode({
    # Request parameters
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'emotion',
    'recognitionModel': 'recognition_01',
    'returnRecognitionModel': 'false',
    'detectionModel': 'detection_01',
})

try:
    conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/detect?%s" % params, '{"url": "https://scontent-lax3-1.cdninstagram.com/v/t51.2885-15/sh0.08/e35/c0.180.1440.1440a/s640x640/88183138_205697387301488_5907001222638953680_n.jpg?_nc_ht=scontent-lax3-1.cdninstagram.com&_nc_cat=1&_nc_ohc=8xgJ9zl2eR0AX9BuIVC&oh=cfdcdd69021381a5289f8a132ac8a410&oe=5E9746C7"}', headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################