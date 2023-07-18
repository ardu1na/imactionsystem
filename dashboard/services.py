##### CONSUMO DE API DE DOLARSI PARA OBTENER EL VALOR DEL BLUE EN TIEMPO REAL

from urllib.request import urlopen
import json

url = "https://www.dolarsi.com/api/api.php?type=dolar"
    
try:
    response = urlopen(url)
    data = json.loads(response.read())
    casa = data[1]
    blue = casa["casa"] 
    venta = float(blue["venta"].replace(',', '.')) # si se desea obtener la compra simplemente es blue["compra"]
except:
    pass
