from flask import Flask, jsonify
from flask_jwt import JWT, jwt_required, current_identity

# si no paso __name__ necesito un __init__.py
server = Flask(__name__)
server.debug = True
server.config['SECRET_KEY'] = 'super-secret'

# implementacion de flask-jwt
from auth_jwt import * 
jwt = JWT(server, authenticate, identity) 

#obj_json = {'user': 'dopel', 'level': 'root'}

@server.route('/')
def index():
    return 'Running' 

@server.route('/jsonify')
@jwt_required()
def json():
    return '%s' % current_identity 


if __name__ == '__main__':
    server.run()
