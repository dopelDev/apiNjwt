from requests import get, post 
from json import dumps, loads

# declara GLOBAL variables
SERVER_URL = 'http://localhost:5000' 
TOKEN = ''

def caller():
    r = get(SERVER_URL + '/jsonify')
    print(r.status_code)
    print(r.text)

def send_post():
    user = {"username": "master", "password": "dopel"}
    headers = {'Content-Type': 'application/json'}
    call_post = post(SERVER_URL + '/auth', data=dumps(user), headers=headers)
    print(call_post.status_code)
    print(call_post.text)
    
    TOKEN = loads(call_post.text)["access_token"]
    return TOKEN

def send_get(TOKEN):
    headers = {'Authorization': 'JWT ' + TOKEN}
    print(TOKEN + 'hola')
    call_get= get(SERVER_URL + '/jsonify', headers=headers)
    print(call_get.status_code)
    print(call_get.text)

if __name__ == '__main__':
    send_get(send_post())
