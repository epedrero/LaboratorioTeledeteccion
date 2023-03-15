#C2RCC
#Librerías y módulos
import snappy
import numpy as np
import os
import zipfile
from snappy import ProductIO, WKTReader, GPF, jpy, HashMap, File
import matplotlib.pyplot as plt

#Lectura de la imagen
path_data = r"C:\Users\ernes\Documents\DatosSat\S3A_OL_1_EFR____20230201T133642_20230201T133942_20230202T135629_0179_095_081_3600_PS1_O_NT_003.zip"
with zipfile.ZipFile(path_data, 'r') as zf:
    zf.extractall(r"C:\Users\ernes\Documents\Laboratorio\Week 5")
    
path_manifesto = r"C:\Users\ernes\Documents\Laboratorio\Week 5\S3A_OL_1_EFR____20230201T133642_20230201T133942_20230202T135629_0179_095_081_3600_PS1_O_NT_003.SEN3\xfdumanifest.xml"
p = snappy.ProductIO.readProduct(path_manifesto)

'''
#Crear .dim a partir del manifesto
### No es necesario, pues se trabaja de igual manera con el manifesto
path_dim = r"C:\Users\ernes\Documents\Laboratorio\Week 5\S3A_OL_1_EFR____20230201T133642_20230201T133942_20230202T135629_0179_095_081_3600_PS1_O_NT_003.dim"
p_dim = ProductIO.writeProduct(p,path_dim,'BEAM-DIMAP')
p_dim_read = ProductIO.readProduct(path_dim)
'''

#Reproyeccion
# Define the WGS84 projection as a WKT string
wgs84_wkt = 'GEOGCS["WGS 84",  DATUM["WGS_1984",    SPHEROID["WGS 84",6378137,298.257223563,      AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,    AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,    AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST],AUTHORITY["EPSG","4326"]]'
               
params_rep = snappy.HashMap()
params_rep.put('targetCRS', wgs84_wkt)
params_rep.put('resampling', 'Nearest')

reprojected_product = GPF.createProduct('Reproject', params_rep,p)

#Subset Lago Villarrica
params = snappy.HashMap()
params.put('copyMetadata', True)
params.put('region','367,3000,91,54') #Esta es la región de interés
subset_p = snappy.GPF.createProduct('Subset', params, p)
subset_path = r"C:\Users\ernes\Documents\Laboratorio\Week 5\subset_of_S3A_OL_1_EFR____20230201T133642_20230201T133942_20230202T135629_0179_095_081_3600_PS1_O_NT_003.dim"
snappy.ProductIO.writeProduct(subset_p, subset_path, 'BEAM-DIMAP')
p_subset = ProductIO.readProduct(subset_path)

#Valores de los parámetros algoritmo c2rcc
sal=35.0
temp=15.0
ozo=330.0
pres=1000.0
el=0.0
TSMfakBpart=1.06
TSMfakBwit=0.942
CHLexp=1.04
CHLfak=21.0
thresholdRtosaOOS=0.01
thresholdAcReflecOos=0.15
thresholdCloudTDown865=0.955
outputAsRrs=False
deriveRwFromPathAndTransmittance=False
useEcmwfAuxData=True
outputRtoa=True
outputRtosaGc=False
outputRtosaGcAann=False
outputRpath=False
outputTdown=False
outputTup=False
outputAcReflectance=True
outputRhown=True
outputOos=False
outputKd=True
outputUncertainties=True

#Ingreso de los parámetros lagoritmo c2rcc
HashMap = jpy.get_type('java.util.HashMap')
parameters = HashMap()
#parameters.put('validPixelExpression','(!quality_flags.invalid && (!quality_flags.land || quality_flags.fresh_inland_water))')
parameters.put('validPixelExpression','quality_flags.fresh_inland_water')
parameters.put('temperature',temp)
parameters.put('salinity',sal)
parameters.put('ozone',ozo)
parameters.put('press',pres)
parameters.put('TSMfakBpart',TSMfakBpart)
parameters.put('TSMfakBwit',TSMfakBwit)
parameters.put('CHLexp',CHLexp)
parameters.put('CHLfak',CHLfak)
parameters.put('thresholdRtosaOOS',thresholdRtosaOOS)
parameters.put('thresholdAcReflecOos',thresholdAcReflecOos)
parameters.put('thresholdCloudTDown865',thresholdCloudTDown865)
parameters.put('outputAsRrs',outputAsRrs)
parameters.put('deriveRwFromPathAndTransmittance',deriveRwFromPathAndTransmittance)
parameters.put('useEcmwfAuxData',useEcmwfAuxData)
parameters.put('outputRtoa',outputRtoa)
parameters.put('outputRtosaGc',outputRtosaGc)
parameters.put('outputRtosaGcAann',outputRtosaGcAann)
parameters.put('outputRpath',outputRpath)
parameters.put('outputTdown',outputTdown)
parameters.put('outputTup',outputTup)
parameters.put('outputAcReflectance',outputAcReflectance)
parameters.put('outputRhown',outputRhown)
parameters.put('outputOos',outputOos)
parameters.put('outputKd',outputKd)
parameters.put('outputUncertainties',outputUncertainties)

#Crear resultado con el algoritmo C2RCC
result = GPF.createProduct('c2rcc.olci', parameters, p_subset)

#Crear .dim del c2rcc
c2rcc_path = r'C:\Users\ernes\Documents\Laboratorio\Week 5\S3A_OL_1_EFR____20230201T133642_20230201T133942_20230202T135629_0179_095_081_3600_PS1_O_NT_003_C2RCC.dim'
ProductIO.writeProduct(result,c2rcc_path,'BEAM-DIMAP')
c2rcc = snappy.ProductIO.readProduct(c2rcc_path)

#Recuperar la banda conc_chl del producto y convertirlo en un array
chl_conc_band = c2rcc.getBand('conc_chl')
width = chl_conc_band.getRasterWidth()
height = chl_conc_band.getRasterHeight()
chl_conc_data = np.zeros(width * height, dtype=np.float32)
chl_conc_band.readPixels(0, 0, width, height, chl_conc_data)
chl_conc_data = chl_conc_data.reshape(height, width)

#Visualizarlo
##Sacar tierra
plt.close('all') #Esto es para limpiar antiguos plots
land_mask = chl_conc_data<0.1
water_mask  = ~land_mask
chl_conc_data[land_mask] = np.nan
##Gráfico
#plt.imshow(chl_conc_data, cmap='jet')
#plt.set_cmap('jet') #
plt.imshow(np.ma.masked_array(chl_conc_data,np.isnan(chl_conc_data)),cmap='jet')
plt.colorbar()
plt.set_cmap('jet') #
plt.imshow(np.ma.masked_array(land_mask, ~land_mask), cmap='gray', alpha=0)
plt.title('Concentración de clorofila en Lago Villarrica')
plt.show()

#Exportar GeoTIFF
geotiff_path = r'C:\Users\ernes\Documents\Laboratorio\Week 5\Subset\subset_snappy_of_S3A_OL_1_EFR____20230201T133642_20230201T133942_20230202T135629_0179_095_081_3600_PS1_O_NT_003.dat'
ProductIO.writeProduct(c2rcc, geotiff_path, 'ENVI')

envi_path = r
ProductIO.writeProduct(c2rcc,)

#path_geo_conc = r"C:\Users\ernes\Documents\Laboratorio\Week 6\conc_chl.tif"
#path_geo_conc_dim = r"C:\Users\ernes\Documents\Laboratorio\Week 6\conc_chl.dim"
#conc_dim = ProductIO.writeProduct(chl_conc_band,path_geo_conc_dim,'BEAM-DIMAP')
#conc_dim_p = ProductIO.readProduct(conc_dim)
#ProductIO.writeProduct(conc_dim_p,path_geo_conc,'GeoTIFF')
