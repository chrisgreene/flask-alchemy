from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from datetime import timedelta

#from livereload import Server, shell
from security import authenticate, identity

from resources.user import UserRegister
from resources.item import Item, ItemList

app = Flask(__name__)
app.debug = True
app.secret_key = 'test'
api = Api(app)
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

#server = Server(app.wsgi_app)
#server.serve()
if __name__ == "__main__": 
  app.run()
