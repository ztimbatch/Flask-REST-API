import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot left blank!'
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='Every item needs a store id'
                        )

    @jwt_required()  # -> activate the login authorization
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'An item with name {name} already exists'}, 400  # Bad request

        data = Item.parser.parse_args()  # we call the parser directly from the class
        item = ItemModel(name, data['price'], data['store_id'])
        # item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'Message': 'An error occured inserting the item'}, 500  # Internal server error
        else:
            return item.json(), 201  # statut creation accepted

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'Message': f'Item {name} deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        items = [item.json() for item in ItemModel.query.all()]
        return {'items': items}, 200 if items else 404
