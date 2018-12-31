from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
import sqlite3

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help="price is required.")

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        print(f"name: {name}")
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        print(f"row{row}")
        if row:
            return {"item": {"name": row[0], "price": row[1]}}

    @jwt_required()
    def get(self, name):
        print(f"user is {current_identity.username}")
        item = Item.find_by_name(name)
        if item:
            return item
        return {"message": "Item not found"}, 404

    def post(self, name):
        if self.find_by_name(name):
            return {"message": "An item with the name '{}' already exists.".format(name)}, 400

        request_data = Item.parser.parse_args()
        item = {"name": name, "price": request_data["price"]}
        print(f"item: {item}")
        try:
            self.insert(item)
        except:
            return {"message": "An error occurred inserting the item."}, 500 

        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?, ?)"
        #cursor.execute(query, (item["name"], item["price"]))
        cursor.execute(query, (item["name"], item["price"]))
        connection.commit()
        connection.close()

    def delete(self, name):
        if self.find_by_name(name) == None:
            return {"message": "Item with the name '{}' doesn't exist.".format(name)}, 400
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name = ?"
        cursor.execute(query, (name,))
        connection.close()
        return {"message": "Item Deleted"}, 201

    def put(self, name):
        request_data = Item.parser.parse_args()
        updated_item = {"name": name, "price": request_data["price"]}
        item = self.find_by_name
        print(f"putting item {item}")

        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message": "An error occurred inserting the item."}, 500
        else: 
            try:
                self.update(updated_item)
            except:
                return {"message": "An error occurred updating the item."}, 500
        return updated_item
    
    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item["price"], item["name"]))
        connection.commit()
        connection.close() 

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({"name": row[0], "price": row[1]})

        connection.close() 
        return items, 200