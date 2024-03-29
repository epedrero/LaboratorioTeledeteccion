from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
import pandas as pd

# connect to the API
user = 'epedrero'
password = 'Maricarmen2023!'
api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')

# Región de interés
geojson_path = r"C:\Users\LABORATORIO\Documents\Ernesto\LaboratorioTeledeteccion\Region\AOI_test.geojson"
footprint = geojson_to_wkt(read_geojson(geojson_path))

products = api.query(footprint,
                     date=(date(2022, 10, 1), date(2023, 5, 14)),
                     platformname='Sentinel-3',
                     producttype='OL_1_EFR___')

products_df = api.to_dataframe(products)
path = r"C:\Users\LABORATORIO\Documents\Ernesto\LaboratorioTeledeteccion\productsimages.xlsx"
products_df.to_excel(path, index=False)
