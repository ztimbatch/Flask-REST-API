import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from ressources.user import UserRegister
from ressources.item import Item, ItemList
from ressources.store import Store, StoreList
from db import db

uri = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
if uri.startswith('postgres'):
    uri = uri.replace('postgres', 'postgresql', 1)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'AFxWZR458962FDSRytmlaFTPPCXW'

db.init_app(app)

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # create a new endpoint /auth

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    app.run(port=5000, debug=True)  # to have a nice message use debug=True
