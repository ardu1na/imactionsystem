import requests

def generate_request(url, params={}):
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()

def get_blue(params={}):
    response = generate_request('https://www.dolarsi.com/api/api.php?type=dolar', params)
    if response:
       blue = response.get('casa')[3]
       return blue.get('nombre').get('Blue')
