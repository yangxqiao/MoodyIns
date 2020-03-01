########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64
def some_func(urls):
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
    fool = {"faceAttributes": {"emotion":
                                   {"anger": 0.0, "contempt": 0.0, "disgust": 0.0, "fear": 0.0, "happiness": 0.0,
                                    "neutral": 0.0, "sadness": 0.0, "surprise": 0.0}}}
    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params,
                     '{"url": "https://i.insider.com/5dcc3df979d7570d633e10ea?width=1100&format=jpeg&auto=webp"}', headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        # anger+=data['faceAttributes']['emotion']['anger']
        # happiness += data['faceAttributes']['emotion']['happiness']
        # print(happiness)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def main():
    some_func(123)
if __name__ == '__main__':
    main()
####################################
