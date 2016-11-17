import requests


def create_100_users():
    for x in range(0, 100):
        json = {
            'username': 'ibrfahim1' + str(x),
            'email': 'emaifl1' + str(x) + "@gamil.com",
            'password': 'asdf'
        }
        requests.post(url="http://127.0.0.1:5000/user", json=json)
