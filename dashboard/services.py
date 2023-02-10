from urllib.request import urlopen
import json
from pprint import pprint


url = "https://www.dolarsi.com/api/api.php?type=dolar"
response = urlopen(url)
data = json.loads(response.read())

casa = data[1]
blue = casa["casa"]
promedio = (float(blue["compra"]) + float(blue["venta"]))/2   
print(promedio)



#desinstalar esta librería y quitarla de inestalled apps y de rerquirements
"""import requests
api_url = "https://www.dolarsi.com/api/api.php?type=dolar"
response = requests.get(api_url)
print (response)"""