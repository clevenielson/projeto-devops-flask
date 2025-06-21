from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_mongoengine import MongoEngine
from mongoengine import NotUniqueError
import re

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

    def validate_cpf(self, cpf):
        # Has the corret mask?
        if not re.match(r'\d{3}\.\d{3}.\d{3}-\d{2}', cpf):
            return False

        # Grab only numbers
        numbers = [int(digit) for digit in cpf if digit.isdigit()]

        # Does it have 11 digits?
        if len(numbers) != 11 or len(set(numbers)) == 1:
            return False

        # Validate first digit after
        sum_of_products = sum(
            a * b for a, b in zip(
                numbers[0:9],
                range(10, 1, -1)
            )
        )
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            return False

        # Validate second digit after -
        sum_of_products = sum(
            a * b for a, b in zip(
                numbers[0:10],
                range(11, 1, -1)
            )
        )
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            return False

        return True

    def post(self):
        data = _user_parse.parse_args()

        if not self.validate_cpf(data["cpf"]):
            return {"message": "CPF is invalid!"}, 400

        try:
            response = UserModel(**data).save()
            return {"message": "User %s successfully created!" % response.id}
        except NotUniqueError:
            return {"message": "CPF already exists in database!"}, 400

    def get(self, cpf: str):
        return {"message": "CPF"}


api.add_resource(Users, '/users')
api.add_resource(User, '/user', '/user/<string:cpf>')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
