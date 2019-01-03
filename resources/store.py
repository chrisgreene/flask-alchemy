from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return {"message": "Store not found"}, 404

    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {"message": "Store '{}' already exists.".format(store.name)}, 400
        else:
            store = StoreModel(name)
            try:
                store.save_to_db()
            except:
                return {"message": "Unable to create store."}, 500

            return {"message": "Store '{}' created.".format(store.name)}, 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            try:
                store.delete_from_db()
            except:
                return {"message": "Unable to delete store."}, 500

            return {"message": "Store '{}' deleted.".format(store.name)}, 201
        else:
            return {"message": "Store '{}' doesn't exist.".format(store.name)}, 400


class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}


