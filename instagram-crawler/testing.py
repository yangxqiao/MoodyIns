import http.client, urllib.request, urllib.parse, urllib.error, base64, json

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
    fool = {"anger": 0.0, "contempt": 0.0, "disgust": 0.0, "fear": 0.0, "happiness": 0.0,
            "neutral": 0.0, "sadness": 0.0, "surprise": 0.0}
    anger = 0
    happiness = 0
    faces = 0
    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        for a in urls:

            # theString = "\'{\"url\": \""+ a +"\"}\'"
            # print(theString)

            # conn.request("POST", "/face/v1.0/detect?%s" % params,
            #              '{"url": "https://i.insider.com/5dcc3df979d7570d633e10ea?width=1100&format=jpeg&auto=webp"}',
            #              headers)
            # print("one")
            # print(a)
            # print(type(a))
            theString = '{\"url\": \"' + a + '\"}'
            #theString = '{\"url\": \"'+ a +'\"}'
            # print(theString)
            conn.request("POST", "/face/v1.0/detect?%s" % params,
                    theString, headers)
            #print("two")

            response = conn.getresponse()
            data = response.read()
            # print(data)
            new_data = data.decode('utf-8')
            # print(new_data)
            # print("before dumps")
            # print(type(new_data))
            # print(new_data)
            new_data = json.loads(new_data)
            # print(new_data)
            # print("after")
            # print(type(new_data))
            # print(new_data)
            # edge cases when images have no faces
            # print(new_data)
            if new_data:
                # print(new_data[0]['faceAttributes']['emotion'])
                # print("dididi")
                for key in new_data[0]['faceAttributes']['emotion']:
                    fool[key] += new_data[0]['faceAttributes']['emotion'][key]
                # print(fool)
                faces += 1
            conn.close()

        for key in fool:
            fool[key]/=faces
        # print(fool)
        return fool

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))