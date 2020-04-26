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
    return render_template('final-homepage.html')

@app.route('/',methods=['POST'])
def getVal():
    hashtag = request.form['hashtag']
    numPost = request.form['numLabel']
    tone = output(get_posts_by_hashtag(hashtag, int(numPost), debug=True))
    print("tone below")
    print(tone)

    # would fall into error when imgtone or txttone is none after executing analyzers
    # and it's very likely to happen


    txtanger, txtfear, txtjoy, txtsadness, txtanalytical, txtconfident, txttentative, txtnotAvailable = 0,0,0,0,0,0,0,0
    if tone[1]:
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
    else:
        txtnotAvailable = 1

    imganger, imgdisgust, imgfear, imghappiness, imgneutral, imgsadness, imgsurprise, imgcontempt, imgnotAvailable = 0,0,0,0,0,0,0,0,0

    if tone[0]:
        imganger = tone[0]['anger']
        imgdisgust = tone[0]['disgust']
        imgfear = tone[0]['fear']
        imghappiness = tone[0]['happiness']
        imgneutral = tone[0]['neutral']
        imgsadness = tone[0]['sadness']
        imgsurprise = tone[0]['surprise']
        imgcontempt = tone[0]['contempt']

    else:
        imgnotAvailable = 1


    url = tone[2]
    post = tone[3]
    imgscores = tone[4]

    anger_scores = []
    happiness_scores = []
    neutral_scores = []
    sadness_scores = []
    for key in imgscores:
        if key is None:
            anger_scores.append(-1)
            happiness_scores.append(-1)
            neutral_scores.append(-1)
            sadness_scores.append(-1)
        else:
            anger_scores.append(key['anger'])
            happiness_scores.append(key['happiness'])
            neutral_scores.append(key['neutral'])
            sadness_scores.append(key['sadness'])

    print("this is tone 4\n")
    print(imgscores)
    print(anger_scores)
    print(happiness_scores)
    print(neutral_scores)
    print(sadness_scores)

    print(imgscores)

    return render_template('final-homepage.html', tone=tone, anger=imganger, disgust=imgdisgust, fear=imgfear,
                           happiness=imghappiness, neutral=imgneutral, sadness=imgsadness, surprise=imgsurprise,
                           contempt=imgcontempt, imgnotAvailable=imgnotAvailable,
                           txtanger=txtanger, txtfear=txtfear, txtjoy=txtjoy, txtsadness=txtsadness,
                           txtanalytical=txtanalytical,
                           txtconfident=txtconfident, txttentative=txttentative, txtnotAvailable=txtnotAvailable,
                           url=url, post=post, imgscores=imgscores,
                           angerscores=anger_scores, happinessscores=happiness_scores, neutralscores=neutral_scores,
                           sadnessscores=sadness_scores
                           )


if __name__ == '__main__':
    app.run(debug=True)