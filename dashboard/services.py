from urllib.request import urlopen
import json

url = "https://www.dolarsi.com/api/api.php?type=dolar"
    
response = urlopen(url)
data = json.loads(response.read())

casa = data[1]
blue = casa["casa"]
compra = float(blue["compra"].replace(',', '.'))
venta = float(blue["venta"].replace(',', '.'))
promedio = (compra + venta)/ 2
