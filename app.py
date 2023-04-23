from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Compatibility(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        return data

api.add_resource(Compatibility, "/compatibility")

if __name__ == "__main__":
    app.run(debug=True)