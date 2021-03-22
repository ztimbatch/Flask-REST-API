import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This field cannot left blank!'
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='This field cannot left blank!'
                        )

    def post(self):
        data = UserRegister.parser.parse_args()  # Get the data from the json payload with the format of the parser

        if UserModel.find_by_username(data['username']):
            return {'Message': 'User already exists'}, 400

        user = UserModel(data['username'], data['password'])
        # user = UserModel(**data)
        user.save_to_db()

        return {'Message': 'User created successfully'}, 201


