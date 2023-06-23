import ee
import urllib.request
import json

# Inicializar Earth Engine
ee.Initialize()

# Leer el archivo GeoJSON
geojson_path = r"C:\Users\ernes\Documents\Laboratorio\LaboratorioTeledeteccion\Region\AOI_test.geojson"
with open(geojson_path) as f:
    geojson_data = json.load(f)

# Extraer la geometría del archivo GeoJSON
geometry = ee.Geometry(geojson_data['features'][0]['geometry'])

# Crear una instancia de la colección Landsat-8 y filtrar imágenes
collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA') \
    .filterBounds(geometry) \
    .filterDate('2021-01-01', '2021-01-20') \
    .sort('CLOUD_COVER')

# Obtener la imagen más reciente de la colección filtrada
image = ee.Image(collection.first())

# Generar una URL para descargar la imagen
url = image.getDownloadURL({
    'scale': 30,  # Resolución espacial en metros
    'region': geometry
})

# Descargar la imagen en tu directorio local
urllib.request.urlretrieve(url, r'C:\Users\ernes\Documents\Laboratorio\LaboratorioTeledeteccion\Resultados_deft\nombre_archivo.png')

