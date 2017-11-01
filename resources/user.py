import sqlite3

from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type = str, required = True, help = "This field cannot be blank!")
        parser.add_argument('password', type = str, required = True, help = "This field cannot be blank!")

        data = parser.parse_args()

        if UserModel.find_by_username(data['username']) is None:
            user = UserModel(data['username'], data['password'])
            user.save_to_db()
            return { 'message' : 'Registration successful' }, 201
        else:
            return { 'message' : 'User exists' }, 409