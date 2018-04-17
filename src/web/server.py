from flask import Flask, render_template
from services.get_nouns_for_date import get_nouns_for_date
from datetime import date

app = Flask(__name__)


@app.route('/')
def root():
    keywords = get_nouns_for_date((date(2016, 1, 1),))
    return render_template('index.html', keywords=keywords)


if __name__ == '__main__':
    app.run(debug=False)
