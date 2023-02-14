from urllib.request import urlopen
import json

url = "https://www.dolarsi.com/api/api.php?type=dolar"



##################################### TO DO ##################################
"""
    HERE WE NEED TO DO SOMETHING FOR ERROR MANAGEMENT 
    MAYBE STORE THE LAST VALID RESPONSE  IN THE DB
    AND DO A
    TRY...[call the api ] save, response
    EXCEPT.. get last valid response
    
"""
##############################################################################
    
response = urlopen(url)
data = json.loads(response.read())

casa = data[1]
blue = casa["casa"]
compra = float(blue["compra"].replace(',', '.'))
venta = float(blue["venta"].replace(',', '.'))
promedio = (compra + venta)/ 2
