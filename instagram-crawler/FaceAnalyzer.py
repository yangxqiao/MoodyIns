import http.client, urllib.request, urllib.parse, urllib.error, base64, json


def faceAnalyzer(urls):
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
    fool = {"anger": 0.0, "contempt": 0.0, "disgust": 0.0, "fear": 0.0, "happiness": 0.0,
            "neutral": 0.0, "sadness": 0.0, "surprise": 0.0}
    anger = 0
    happiness = 0
    faces = 0
    try:
        individualTones = []
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        for a in urls:

            theString = '{\"url\": \"' + a + '\"}'
            conn.request("POST", "/face/v1.0/detect?%s" % params,
                         theString, headers)

            response = conn.getresponse()
            data = response.read()
            new_data = data.decode('utf-8')
            new_data = json.loads(new_data)
            # edge cases when images have no faces
            print("printing new_data")
            print(new_data)
            if new_data:
                # print(new_data[0]['faceAttributes']['emotion'])
                # print("dididi")
                for key in new_data[0]['faceAttributes']['emotion']:
                    fool[key] += new_data[0]['faceAttributes']['emotion'][key]
                # print(fool)
                faces += 1
                individualTones.append(new_data[0]['faceAttributes']['emotion'])
            else:
                individualTones.append(None)
            conn.close()

        for key in fool:
            fool[key] /= faces
        # print(fool)
        return fool, individualTones

    except Exception as e:
        print(e)
