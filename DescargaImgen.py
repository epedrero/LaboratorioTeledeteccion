import sentinelsat
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
import os

# Configurar la API
api = SentinelAPI('epedrero', 'Maricarmen2023!', 'https://scihub.copernicus.eu/dhus')

# Definir área de interés
geojson_path = r"C:\Users\ernes\Documents\Laboratorio\Week 6\AOI_test.geojson"
footprint = geojson_to_wkt(read_geojson(geojson_path))

# Buscar los productos
products = api.query(footprint,
                     date=('20190101', '20190201'),
                     platformname='Sentinel-3',
                     producttype='SL_1_RBT')

# Descargar los productos encontrados
api.download_all(products, directory_path=r'C:\Users\ernes\Documents\Laboratorio\LaboratorioTeledeteccion\Resultados deft')

# Extraer los archivos ZIP descargados
for product in products:
    # Nombre del archivo ZIP descargado
    zip_file = api.get_product_odata(product)['title']
    # Extraer el archivo ZIP
    os.system(f'unzip {zip_file}')