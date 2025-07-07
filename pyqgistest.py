import sys
import os
from qgis.core import *
from qgis import processing
from qgis.analysis import QgsNativeAlgorithms


# Supply path to qgis install location
#path = r"C:\Program Files\QGIS 3.34.12\apps\qgis-ltr"      # Windows
path = r"~/usr"                                              # Ubuntu
QgsApplication.setPrefixPath(path, True)

# Create a reference to the QgsApplication.  Setting the
# second argument to False disables the GUI.
os.environ["QT_QPA_PLATFORM"] = "offscreen"
qgs = QgsApplication([], False)

# Initialize a QGIS instance
qgs.initQgis()

#sys.path.append(r"C:\Program Files\QGIS 3.34.12\apps\qgis-ltr\python\plugins")     # Windows
sys.path.append('/usr/share/qgis/python/plugins')                                   # Ubuntu

import processing
from processing.core.Processing import Processing
Processing.initialize()

project = QgsProject.instance()
project.read('./TransitConnectivity.qgz')
print("test")
print(f"layer count: {project.count()}, base name: {project.baseName()}")
#for name in project.mapLayers().values():
#    print(layer.name())

from AlgorithmProvider import AlgorithmProvider
Processing.initialize()
provider = AlgorithmProvider()
QgsApplication.processingRegistry().addProvider(provider)
#QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
#
#
params = {
        'STARTLOCATION'     : '7642700.835310,682883.097856 [EPSG:2913]',
        'SEARCHTIMELIMIT'   : 15,
        'OUTPUT'            : 'TEMPORARY_OUTPUT'
        }

feedback = QgsProcessingFeedback()
result = processing.run("alg_provider:transitservicearea", params)
#
#
# # Finally, exitQgis() is called to remove the
# # provider and layer registries from memory
qgs.exitQgis()
