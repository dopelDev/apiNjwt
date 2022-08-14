import jwt
from datetime import datetime
from functools import wraps
from flask import jsonify, request
from time import sleep

# dumb key
MY_SECRET_KEY = 'bloodywood'


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id
    
    def __getitem__(self, id):
        return "User(id='%s')" % self.id
    

users = [User(0, 'master', 'dopel'),
        User(1,'slave', 'nani')]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def create_token(payload: dict):
    token = jwt.encode({'user' : payload.user, 'password' : payload.password,
        'exp': datetime.utcnow() + datetime.timedelta(minutes=4)}, key = MY_SECRET_KEY,
        algorithm = 'HS256')
    return jsonify({'token' : token})

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token =  request.args.get('token')
        user = request.args.get('user')
        password = request.args.get('password')
        if not token:
            return jsonify({'message' : 'token is missing'})
        elif user in username_table:
            user = username_table.get(user, None)
            print(user)
            return jsonify({'message' : 'User is found'})
            if password == user.password:
               try:
                   data = jwt.decode(token, MY_SECRET_KEY, algorithms='HS256')
               except:
                    return jsonify({'messege' : 'token is valid'})
        else: 
            return jsonify({'message' : 'User dont found'})
        return func(*args, **kwargs)
    return decorated
            

