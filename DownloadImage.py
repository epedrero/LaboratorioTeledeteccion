from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date

# connect to the API
user = 'epedrero'
password = 'Maricarmen2023!'
api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')

# Region
geojson_path = r"C:\Users\LABORATORIO\Documents\Ernesto\LaboratorioTeledeteccion\Region\AOI_test.geojson"
footprint = geojson_to_wkt(read_geojson(geojson_path))

products = api.query(footprint,
                     date=(date(2022, 10, 1), date(2023, 5, 14)),
                     platformname='Sentinel-3',
                     producttype='OL_1_EFR___')

'''
# Download
path_download=r"C:\Users\ernes\Documents\Laboratorio\LaboratorioTeledeteccion\Resultados deft\data_download"
products_df = api.to_dataframe(products)
api.download_all(products_df.index,directory_path=path_download)
'''