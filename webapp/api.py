import requests


def get_token():

    request_data = {'login': 'login', 'type': 'patient', 'password': 'password'}

    headers = {'Content-Type': 'application/json'}

    response = requests.post('url', params=request_data, headers=headers)

    result = response.json()

    token = result['token']

    return token
