from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
import pandas as pd
import rasterio

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
                     platformname='Sentinel-2',
                     producttype='S2MSI1C' # Productos de Sentinel-2 multibanda
                     )

# Abrir el producto con rasterio
with rasterio.open(products.path) as src:
    # Obtener las bandas 11, 12 y 8
    b11 = src['B11']
    b12 = src['B12']
    b8 = src['B8']


'''
# Descargar los productos encontrados
api.download_all(products)
'''