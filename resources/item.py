from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help="price is required.")
    parser.add_argument("store_id", type=int, required=True, help="store_id is required.")

    @jwt_required()
    def get(self, name):
        #print(f"user is {current_identity.username}")
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with the name '{}' already exists.".format(name)}, 400

        request_data = Item.parser.parse_args()
        item = ItemModel(name, request_data["price"], request_data["store_id"])
        #print(f"item: {item}")
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500 

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        # if ItemModel.find_by_name(name) == None:
        #     return {"message": "Item with the name '{}' doesn't exist.".format(name)}, 400
        
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "DELETE FROM items WHERE name = ?"
        # cursor.execute(query, (name,))
        # connection.commit()
        # connection.close()
        return {"message": "Item Deleted"}, 200

    @jwt_required()
    def put(self, name):
        request_data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        #print(f"item: {item}")
        if item is None:
            item = ItemModel(name, request_data["price"], request_data["store_id"])
        else: 
            item.price = request_data["price"] 
            item.store_id = request_data["store_id"] 

        item.save_to_db()
        return item.json()
    
    
class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}
