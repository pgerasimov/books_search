import requests


def get_token():

    request_data = {'login': '79260657755', 'type': 'patient', 'password': 'aft453kt'}

    headers = {'Content-Type': 'application/json'}

    response = requests.post('https://api.ibolit.pro/api/v3/check-password', params=request_data, headers=headers)

    result = response.json()

    token = result['token']

    return token
