from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from security import authenticate, identity

from resources.user import UserRegister

from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type = float, required = True, help = "The price field cannot be blank!")
    parser.add_argument('store_id', type = int, required = True, help = "The store_id field cannot be blank!")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return { 'message' : 'Item does not exist' }, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return { 'message' : 'An Item with name "{}" already exists'.format(name) }, 409
        else:
            request_data = Item.parser.parse_args()
            # could be replaced by ItemModel(name, **data)
            item = ItemModel(name, request_data['price'], request_data['store_id'])
            try:
                item.save_to_db()
            except:
                return { "message" : "An error occured while inserting this item" }, 500
            return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        
        return { 'message' : 'Item deleted' }

    def put(self, name):
        request_data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            # could be replaced by ItemModel(name, **data)
            item = ItemModel(name, request_data['price'], request_data['store_id'])
        else:
            item.price = request_data['price']
            item.store_id = request_data['store_id']
        item.save_to_db()
        
        return item.json()

class ItemList(Resource):
    def get(self):
        return [item.json() for item in ItemModel.query.all()]