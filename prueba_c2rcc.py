import snappy
import os
from snappy import ProductIO, WKTReader, GPF, jpy, HashMap, File
import matplotlib.pyplot as plt
import zipfile

path_data= r"C:\Users\ernes\Documents\DatosSat\S3A_OL_1_EFR____20230201T133642_20230201T133942_20230202T135629_0179_095_081_3600_PS1_O_NT_003.zip"

with zipfile.ZipFile(path_data, 'r') as zf:
    zf.extractall(r"C:\Users\ernes\Documents\Laboratorio\Week 5")

path_manifesto = r"C:\Users\ernes\Documents\Laboratorio\Week 5\S3A_OL_1_EFR____20230201T133642_20230201T133942_20230202T135629_0179_095_081_3600_PS1_O_NT_003.SEN3\xfdumanifest.xml"

p = snappy.ProductIO.readProduct(path_manifesto)

sal=35.0
temp=15.0
ozo=330.0
pres=1000.0
el=0.0
TSMfakBpart=1.72
TSMfakBwit=3.1
CHLexp=1.04
CHLfak=21.0
thresholdRtosaOOS=0.005
thresholdAcReflecOos=0.1
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

HashMap = jpy.get_type('java.util.HashMap')
parameters = HashMap()
#parameters.put('validPixelExpression','(!quality_flags.invalid && (!quality_flags.land || quality_flags.fresh_inland_water)')
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

result = GPF.createProduct('c2rcc', parameters, p)
product=ProductIO.writeProduct(result,r'C:\Users\ernes\Documents\Laboratorio\Week 5\Result_S3_C2RCC.dim','BEAM-DIMAP')
