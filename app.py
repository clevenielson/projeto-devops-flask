from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_mongoengine import MongoEngine

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'users',
    'port': 27017,
    'host': 'mongodb',
    'username': 'admin',
    'password': 'senha123'
}

_user_parse = reqparse.RequestParser()
_user_parse.add_argument(
    'first_name',
    type=str,
    required=True,
    help="This field cannot be blank."
)
_user_parse.add_argument(
    'last_name',
    type=str,
    required=True,
    help="This field cannot be black."
)
_user_parse.add_argument(
    'cpf',
    type=str,
    required=True,
    help="This field cannot be black."
)
_user_parse.add_argument(
    'email',
    type=str,
    required=True,
    help="This field cannot be black."
)
_user_parse.add_argument(
    'birth_date',
    type=str,
    required=True,
    help="This field cannot be black."
)

api = Api(app)
db = MongoEngine(app)


# Modelo de usuario
class UserModel(db.Document):
    cpf = db.StringField(required=True, unique=True)
    email = db.StringField(required=True)
    first_name = db.StringField(required=True, max_length=50)
    last_name = db.StringField(required=True, max_length=50)
    birth_date = db.StringField(required=True)


class Users(Resource):
    def get(self):
        return {"message": "user 1"}


class User(Resource):
    def post(self):
        data = _user_parse.parse_args()
        UserModel(**data).save()

    def get(self, cpf: str):
        return {"message": "CPF"}


api.add_resource(Users, '/users')
api.add_resource(User, '/user', '/user/<string:cpf>')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
