from flask import Flask, jsonify, request
import auth_jwt

# si no paso __name__ necesito un __init__.py
server = Flask(__name__)
server.debug = True
server.config['SECRET_KEY'] = 'super-secret'

# implementacion de flask-jwt

@server.route('/')
def index():
    return 'Running' 

@server.route('/jsonify')
@auth_jwt.token_required
def json():
    return jsonify({'message' : 'data secret'}) 

@server.route('/auth', methods = ['GET', 'POST'])
def auth(): 
    if request.method == 'GET':
        return jsonify({'message' : 'end point for verified'})
    if request.method == 'POST':
        data = request.data
        headers = request.headers
        if headers.get('Content-Type') == 'application/json':
            pass
        return jsonify({'message' : 'work'})

if __name__ == '__main__':
    server.run()
