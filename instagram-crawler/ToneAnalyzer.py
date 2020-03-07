from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
# from crawler.py import output


def toneAnalyzer(text):
    # print(text)
    authenticator = IAMAuthenticator('Wxw1mVFTAI3bWwDrZ1XtoM03pWvbdZo5pNiTt1YsO17y')
    tone_analyzer = ToneAnalyzerV3(
        version='2017-09-21',
        authenticator=authenticator
    )
    # print("This")

    # tone_analyzer.set_service_url('https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/28e8a715-3ae4-45b5-a691-0d388f58e276')
    tone_analyzer.set_service_url('https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/28e8a715-3ae4-45b5-a691-0d388f58e276')

    # text = output()
    # print("This")

    tone_analysis = tone_analyzer.tone(
        {'text': text},
        content_type='application/json'
    ).get_result()
    #dictTones = json.loads(json.dumps(tone_analysis, indent=2))
    #dictTones = json.loads(tone_analysis)
    # print("This")
    # print(tone_analysis)
    # print(tone_analysis['document_tone'])
    return tone_analysis['document_tone']
