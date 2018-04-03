from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class Words(Resource):
    def get(self):
        return ["some", "words", "I", "don't", "care", "about", "this", "for", "now"]


api.add_resource(Words, '/words')


if __name__ == '__main__':
    app.run(debug=True)
