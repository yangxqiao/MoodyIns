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
    # url = {'url1': tone[2][0], 'url2': tone[2][1], 'url3': tone[2][2], 'url4': tone[2][3], 'url5': tone[2][4], 'url6': tone[2][5], 'url7': tone[2][6], 'url8': tone[2][7], 'url9': tone[2][8]}
    # post = {'post1': tone[3][0], 'post2': tone[3][1], 'post3': tone[3][2], 'post4': tone[3][3], 'post5': tone[3][4], 'post6': tone[3][5], 'post7': tone[3][6], 'post8': tone[3][7], 'post9': tone[3][8]}

    return render_template('final-homepage.html', tone = tone, anger = imganger, disgust = imgdisgust, fear = imgfear,
                           happiness = imghappiness, neutral = imgneutral, sadness = imgsadness, surprise = imgsurprise,
                            contempt = imgcontempt, imgnotAvailable = imgnotAvailable,
                           txtanger = txtanger, txtfear = txtfear, txtjoy = txtjoy, txtsadness = txtsadness,
                           txtanalytical = txtanalytical,
                           txtconfident = txtconfident, txttentative = txttentative, txtnotAvailable = txtnotAvailable,
                           #  url1 = tone[2][0], url2 = tone[2][1], url3 = tone[2][2], url4 = tone[2][3], url5 = tone[2][4],
                           # post1=tone[3][0], post2=tone[3][1], post3=tone[3][2], post4=tone[3][3], post5=tone[3][4]
                           url = url, post = post, imgscores = imgscores
                           )

if __name__ == '__main__':
    app.run(debug=True)