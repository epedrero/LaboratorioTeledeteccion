import snappy
from snappy import ProductIO, WKTReader
from snappy import jpy
from snappy import GPF
from snappy import HashMap

# setting the aggregator method
aggregator_average_config = snappy.jpy.get_type('org.esa.snap.binning.aggregators.AggregatorAverage$Config')
agg_avg_chl = aggregator_average_config('CHL_NN')

# creating the hashmap to store the parameters
HashMap = snappy.jpy.get_type('java.util.HashMap')
parameters = HashMap()

#creating the aggregator array
aggregators = snappy.jpy.array('org.esa.snap.binning.aggregators.AggregatorAverage$Config', 1)
#adding my aggregators in the list
aggregators[0] = agg_avg_chl

# set parameters
# output directory 
dir_out = r'C:\Users\ernes\Documents\DatosSat\level-3_py_dynamic.dim'
parameters.put('outputFile', dir_out)

# number of rows (directly linked with resolution)
parameters.put('numRows', 66792) # to have about 300 meters spatial resolution

# aggregators list
parameters.put('aggregators', aggregators)

# Region to clip the aggregation on
wkt="POLYGON ((8.923302175377243 59.55648108694149, 13.488748662344074 59.11388968719029,12.480488185001589 56.690625338725155, 8.212366327767503 57.12425256476263,8.923302175377243 59.55648108694149))"
geom = WKTReader().read(wkt)
parameters.put('region', geom)

# Source product path 
path_15 = r"C:\Users\ernes\Documents\DatosSat\S3A_OL_2_WFR____20230212T135139_20230212T135439_20230212T153550_0179_095_238_3600_MAR_O_NR_003.SEN3\S3A_OL_2_WFR____20230212T135139_20230212T135439_20230212T153550_0179_095_238_3600_MAR_O_NR_003.SEN3\xfdumanifest.xml"
#path_16 = r"C:\Users\ernes\Documents\DatosSat\S3B_OL_2_WFR____20201016.SEN3\xfdumanifest.xml"
#path = path_15 + "," + path_16
parameters.put('sourceProductPaths', path_15)

#result = snappy.GPF.createProduct('Binning', parameters, (source_p1, source_p2))

# create results
result = snappy.GPF.createProduct('Binning', parameters) #to be used with product paths specified in the parameters hashmap

print("results stored in: {0}".format(dir_out) )
