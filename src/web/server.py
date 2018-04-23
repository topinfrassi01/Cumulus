from flask import Flask, render_template, request
from services.get_keywords_for_date import get_keywords_for_date
from services.get_articles import get_articles
from datetime import date
from urllib import parse
import json

app = Flask(__name__)


@app.route('/')
def root():
    keywords = get_keywords_for_date((date(2017, 2, 3),))
    return render_template('index.html', keywords=keywords[0:30])


@app.route('/keyword')
@app.route('/keyword/ids=<ids>')
def keyword(ids):
    ids = json.loads(ids[1:-1])

    articles = get_articles(ids)

    return render_template("keywords.html", articles=articles)


if __name__ == '__main__':
    app.run(debug=False)
