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


    txtanger, txtfear, txtjoy, txtsadness, txtanalytical, txtconfident, txttentative = 0,0,0,0,0,0,0

    for i in tone[1]['tones']:
        if i['tone_id'] == 'anger':
            txtanger = i['score']
        if i['tone_id'] == 'fear':
            txtfear = i['score']
        if i['tone_id'] == 'joy':
            txtjoy = i['score']
        if i['tone_id'] == 'sadness':
            txtsadness = i['score']
        if i['tone_id'] == 'analytical':
            txtanalytical = i['score']
        if i['tone_id'] == 'confident':
            txtconfident = i['score']
        if i['tone_id'] == 'tentative':
            txttentative = i['score']

    imganger, imgdisgust, imgfear, imghappiness, imgneutral, imgsadness, imgsurprise = 0,0,0,0,0,0,0

    if tone[0]:
        imganger = tone[0]['anger']
        imgdisgust = tone[0]['disgust']
        imgfear = tone[0]['fear']
        imghappiness = tone[0]['happiness']
        imgneutral = tone[0]['neutral']
        imgsadness = tone[0]['sadness']
        imgsurprise = tone[0]['surprise']

    return render_template('pass.html',tone = tone, anger = imganger, disgust = imgdisgust, fear = imgfear,
                           happiness = imghappiness,neutral = imgneutral, sadness = imgsadness, surprise = imgsurprise,

                           txtanger = txtanger, txtfear = txtfear, txtjoy = txtjoy, txtsadness = txtsadness,
                           txtanalytical = txtanalytical,
                           txtconfident = txtconfident, txttentative = txttentative
                           )

if __name__ == '__main__':
    app.run(debug=True)
