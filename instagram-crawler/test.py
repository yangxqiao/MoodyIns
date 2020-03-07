from flask import Flask, render_template, request
from inscrawler import InsCrawler
from inscrawler.settings import override_settings
from inscrawler.settings import prepare_override_settings
from ToneAnalyzer import toneAnalyzer
from testing import some_func
from templates.crawler import get_posts_by_hashtag, output

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('homepage_test.html')

@app.route('/',methods=['POST'])

def getVal():
    hashtag = request.form['hashtag']
    happy = output(get_posts_by_hashtag(hashtag, 5, debug=True))
    return render_template('pass.html',h = happy)

if __name__ == '__main__':
    app.run(debug=True)