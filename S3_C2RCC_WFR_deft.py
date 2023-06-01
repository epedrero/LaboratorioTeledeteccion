import snappy
from sentinelsat import SentinelAPI, geojson_to_wkt, read_geojson
import numpy as np
import matplotlib.pyplot as plt
#import os
#import numpy as np
from snappy import (ProgressMonitor, VectorDataNode,
                    WKTReader, ProductIO, PlainFeatureFactory,
                    SimpleFeatureBuilder, DefaultGeographicCRS,
                    ListFeatureCollection, FeatureUtils,jpy, HashMap, File,GPF)

"""Search S3 EFR product"""


"""Read S3 EFR product from Local folder"""
s3efr_path = r"C:\Users\ernes\Documents\DatosSat"
s3efr_filename = r"\S3A_OL_1_EFR____20230201T133642_20230201T133942_20230202T135629_0179_095_081_3600_PS1_O_NT_003\S3A_OL_1_EFR____20230201T133642_20230201T133942_20230202T135629_0179_095_081_3600_PS1_O_NT_003.SEN3\xfdumanifest.xml"
s3efr = ProductIO.readProduct(s3efr_path+s3efr_filename)

"""Read Area Of Interest (AOI) """
geojson_path = r"C:\Users\ernes\Documents\Laboratorio\Week 6\AOI_test.geojson"
aoi = geojson_to_wkt(read_geojson(geojson_path))
geometry = WKTReader().read(aoi)
geometry_parameters = HashMap()
geometry_parameters.put("copyMetadata", True)
geometry_parameters.put("geoRegion", geometry)

"""Create a Subset using AOI"""
subset_s3efr = snappy.GPF.createProduct('Subset', geometry_parameters, s3efr)
subset_s3efr_dst = r"C:\Users\ernes\Documents\Laboratorio\LaboratorioTeledeteccion\Resultados deft\subset_s3efr.dim"
product_s3efr=snappy.ProductIO.writeProduct(subset_s3efr, subset_s3efr_dst, 'BEAM-DIMAP')
product_s3efr=snappy.ProductIO.readProduct(subset_s3efr_dst)

""" Create Cloud Mask using IdePix S3 OLCI"""
idepix_parameters = HashMap()
idepix_parameters.put('radianceBandsToCopy','Oa01_radiance,Oa02_radiance,Oa03_radiance,Oa04_radiance,Oa05_radiance,Oa06_radiance,Oa07_radiance,Oa08_radiance,Oa09_radiance,Oa10_radiance,Oa11_radiance,Oa12_radiance,Oa13_radiance,Oa14_radiance,Oa15_radiance,Oa16_radiance,Oa17_radiance,Oa18_radiance,Oa19_radiance,Oa20_radiance,Oa21_radiance')
idepix_parameters.put('computeCloudShadow','true')
idepix_parameters.put('outputCtp','false')
idepix_parameters.put('computeCloudBuffer','true')
idepix_parameters.put('CloudBufferWidth',2)
idepix_parameters.put('useSrtmLandWaterMaske','false')

idepix_product = GPF.createProduct('Idepix.OLCI',idepix_parameters, subset_s3efr)
idepix_dst = r"C:\Users\ernes\Documents\Laboratorio\LaboratorioTeledeteccion\Resultados deft\idepix.dim"
snappy.ProductIO.writeProduct(idepix_product, idepix_dst, 'BEAM-DIMAP')
idepix_product_read = snappy.ProductIO.readProduct(idepix_dst)


"""Cloud mask apply"""
# Aplicar corrección de órbita
params_cloud = snappy.HashMap()
params_cloud.put('orbitType', 'Sentinel Restituted (Auto Download)')
params_cloud.put('polyDegree', '3')
corrected_product = GPF.createProduct('Apply-Orbit-File', params_cloud, product)

# Mask apply
params = snappy.HashMap()
params.put('landMask', mask)
params.put('cloudMask', mask)
params.put('invalidMask', mask)
masked_product = GPF.createProduct('Meris.Mask', params, corrected_product)

# Save mask applied
ProductIO.writeProduct(masked_product, r'C:\Users\ernes\Documents\Laboratorio\LaboratorioTeledeteccion\Resultados deft\masked.dim', 'BEAM-DIMAP')

"""C2RCC Algorithm params"""
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

"""C2RCC algorithm"""
HashMap = jpy.get_type('java.util.HashMap')
c2rcc_parameters = HashMap()
#c2rcc_parameters.put('validPixelExpression','(!quality_flags.invalid && (!quality_flags.land || quality_flags.fresh_inland_water))')
c2rcc_parameters.put('validPixelExpression', 'quality_flags.fresh_inland_water')
c2rcc_parameters.put('temperature', temp)
c2rcc_parameters.put('salinity', sal)
c2rcc_parameters.put('ozone', ozo)
c2rcc_parameters.put('press', pres)
c2rcc_parameters.put('TSMfakBpart', TSMfakBpart)
c2rcc_parameters.put('TSMfakBwit', TSMfakBwit)
c2rcc_parameters.put('CHLexp', CHLexp)
c2rcc_parameters.put('CHLfak', CHLfak)
c2rcc_parameters.put('thresholdRtosaOOS', thresholdRtosaOOS)
c2rcc_parameters.put('thresholdAcReflecOos', thresholdAcReflecOos)
c2rcc_parameters.put('thresholdCloudTDown865', thresholdCloudTDown865)
c2rcc_parameters.put('outputAsRrs', outputAsRrs)
c2rcc_parameters.put('deriveRwFromPathAndTransmittance', deriveRwFromPathAndTransmittance)
c2rcc_parameters.put('useEcmwfAuxData', useEcmwfAuxData)
c2rcc_parameters.put('outputRtoa', outputRtoa)
c2rcc_parameters.put('outputRtosaGc', outputRtosaGc)
c2rcc_parameters.put('outputRtosaGcAann', outputRtosaGcAann)
c2rcc_parameters.put('outputRpath', outputRpath)
c2rcc_parameters.put('outputTdown', outputTdown)
c2rcc_parameters.put('outputTup', outputTup)
c2rcc_parameters.put('outputAcReflectance', outputAcReflectance)
c2rcc_parameters.put('outputRhown', outputRhown)
c2rcc_parameters.put('outputOos', outputOos)
c2rcc_parameters.put('outputKd', outputKd)
c2rcc_parameters.put('outputUncertainties', outputUncertainties)

"""S3 Water Full Resolution (WFR) product"""
s3wfr = GPF.createProduct('c2rcc.olci', c2rcc_parameters, subset_s3efr)
s3wfr_dst = r"C:\Users\ernes\Documents\Laboratorio\LaboratorioTeledeteccion\Resultados deft\s3wfr.dim"
snappy.ProductIO.writeProduct(s3wfr, s3wfr_dst, 'BEAM-DIMAP')

"""Reprojection"""
reprojec_parameters = HashMap()
reprojec_parameters.put('crs', '4326')
reprojec_parameters.put('noDataValue', -9999.)
reprojec_parameters.put('addDeltaBands', False)

s3wfr_reproject = GPF.createProduct('Reproject', reprojec_parameters, s3wfr)
s3wfr_reproject_dst = r"C:\Users\ernes\Documents\Laboratorio\LaboratorioTeledeteccion\Resultados deft\reprojec.dim"
snappy.ProductIO.writeProduct(s3wfr_reproject, s3wfr_reproject_dst, 'BEAM-DIMAP')
s3wfr_reproject_dst_read = snappy.ProductIO.readProduct(s3wfr_reproject_dst)

""""Plot"""
chl_conc_band = s3wfr_reproject_dst_read.getBand('conc_chl')
width = chl_conc_band.getRasterWidth()
height = chl_conc_band.getRasterHeight()
chl_conc_data = np.zeros(width * height, dtype=np.float32)
chl_conc_band.readPixels(0, 0, width, height, chl_conc_data)
chl_conc_data = chl_conc_data.reshape(height, width)


plt.close('all') #Esto es para limpiar antiguos plots
land_mask = chl_conc_data<0.01
water_mask  = ~land_mask
chl_conc_data[land_mask] = np.nan
##Gráfico
#plt.imshow(chl_conc_data, cmap='jet')
#plt.set_cmap('jet') #
plt.imshow(np.ma.masked_array(chl_conc_data, np.isnan(chl_conc_data)), cmap='jet')
plt.colorbar()
plt.set_cmap('jet')
plt.imshow(np.ma.masked_array(land_mask, ~land_mask), cmap='gray', alpha=0)
plt.title('Chlorophyll-$a$ concentration in the Villarrica Lake zone')
plt.show()