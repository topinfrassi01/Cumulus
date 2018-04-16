from flask import Flask
from flask_restful import Resource, Api
from services.get_nouns_for_date import get_nouns_for_date
from datetime import date
from flask_cors import CORS


app = Flask(__name__)
api = Api(app)
CORS(app)


class Words(Resource):
    def get(self):
        nouns = get_nouns_for_date((date(2016,1,1),))

        nouns = sorted(nouns.items(), key=lambda x: len(x[1]))
        nouns.reverse()
        return nouns[0:10]

class Main(Resource):
    def get(self):
        return [1,2,3]

api.add_resource(Words, '/words')
api.add_resource(Main, '/')


if __name__ == '__main__':
    app.run(debug=False)
