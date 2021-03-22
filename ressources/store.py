from flask_restful import Resource, reqparse
from models.store import StoreModel


class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        else:
            return {'Message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'Message': f'A Store with a name {name} already exists'}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except :
            return {'Message': 'An error occured while creating store'}, 500
        else:
            return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'Message': 'Store deleted'}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
