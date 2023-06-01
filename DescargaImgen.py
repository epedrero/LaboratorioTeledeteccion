import sentinelsat
import pandas
import collections
from collections import OrderedDict
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
import os

# API settings
user = 'epedrero'
password = 'Maricarmen2023!'
url = 'https://scihub.copernicus.eu/dhus'
api = SentinelAPI(user, password, url)

# Region
geojson_path = r"C:\Users\ernes\Documents\Laboratorio\Week 6\AOI_test.geojson"
footprint = geojson_to_wkt(read_geojson(geojson_path))

# Search the products
products = api.query(footprint,
                     date=('20190101', '20190201'),
                     platformname='Sentinel-3',
                     cloudcoverpercentage=(0, 0),
                     producttype='SR_2_WAT',
                     filename='S3*.SEN3',
                     )

# download single scene by known product id
#product_id = list(products.keys())[0]
#products=api.download('f634aac4-ecc5-48da-a0fa-e1671ead0a86')

# Descargar los productos encontrados
api.download_all(products, directory_path=r'C:\Users\ernes\Documents\Laboratorio\LaboratorioTeledeteccion\Resultados deft')

# Extraer los archivos ZIP descargados
for product in products:
    # Nombre del archivo ZIP descargado
    zip_file = api.get_product_odata(product)['title']
    # Extraer el archivo ZIP
    os.system(f'unzip {zip_file}')

products_df = api.to_dataframe(products)