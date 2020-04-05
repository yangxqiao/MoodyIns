from flask import Flask, render_template, request
from inscrawler import InsCrawler
from inscrawler.settings import override_settings
from inscrawler.settings import prepare_override_settings
from ToneAnalyzer import toneAnalyzer
from FaceAnalyzer import faceAnalyzer
from templates.crawler import get_posts_by_hashtag, output

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('homepage_test.html')

@app.route('/',methods=['POST'])
def getVal():
    hashtag = request.form['hashtag']
    tone = output(get_posts_by_hashtag(hashtag, 5, debug=True))
    print("tone below")
    print(tone)

    # would fall into error when imgtone or txttone is none after executing analyzers
    # and it's very likely to happen
    anger, fear, joy, sadness, analytical, confident, tentative = 0,0,0,0,0,0,0

    for i in tone[1]['tones']:
        if i['tone_id'] == 'anger':
            anger = i['score']
        if i['tone_id'] == 'fear':
            fear = i['score']
        if i['tone_id'] == 'joy':
            joy = i['score']
        if i['tone_id'] == 'sadness':
            sadness = i['score']
        if i['tone_id'] == 'analytical':
            analytical = i['score']
        if i['tone_id'] == 'confident':
            confident = i['score']
        if i['tone_id'] == 'tentative':
            tentative = i['score']

    return render_template('pass.html',tone = tone, anger = tone[0]['anger'], disgust = tone[0]['disgust'], fear = tone[0]['fear'], happiness = tone[0]['happiness'],
                           neutral = tone[0]['neutral'], sadness = tone[0]['sadness'], surprise = tone[0]['surprise'],
                           txtanger = anger, txtfear = fear, txtjoy = joy, txtsadness = sadness, txtanalytical = analytical,
                           txtconfident = confident, txttentative = tentative
                           )

if __name__ == '__main__':
    app.run(debug=True)
