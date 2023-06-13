from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
import pandas as pd

# Conectar a la API
user = 'epedrero'
password = 'Maricarmen2023!'
api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')

# Región de interés
geojson_path = r"C:\Users\LABORATORIO\Documents\Ernesto\LaboratorioTeledeteccion\Region\AOI_test.geojson"
footprint = geojson_to_wkt(read_geojson(geojson_path))

# Consulta de productos
products = api.query(footprint,
                     date=(date(2022, 10, 1), date(2023, 5, 14)),
                     platformname='Sentinel-3',
                     producttype='SL_2_LST___' # Productos de temperatura superficial del agua
                     )

products_df = api.to_dataframe(products)
for column in products_df.columns:
    print(column)
path = r"C:\Users\LABORATORIO\Documents\Ernesto\LaboratorioTeledeteccion\products.xlsx"
products_df.to_excel(path, index=False)
'''
# Descargar los productos encontrados
api.download_all(products)
'''