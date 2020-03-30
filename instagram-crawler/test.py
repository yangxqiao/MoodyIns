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
    return render_template('pass.html',tone = tone, anger = tone[0]['anger'], disgust = tone[0]['disgust'], fear = tone[0]['fear'], happiness = tone[0]['happiness'], neutral = tone[0]['neutral'], sadness = tone[0]['sadness'], surprise = tone[0]['surprise'], txtToneId = tone[1]['tones'][0]['tone_id'], txtToneScore = tone[1]['tones'][0]['score'])

if __name__ == '__main__':
    app.run(debug=True)
