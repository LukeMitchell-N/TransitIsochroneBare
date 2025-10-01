import sys
import os
from qgis.core import *
from qgis import processing
from qgis.analysis import QgsNativeAlgorithms
from datetime import datetime
#sys.path.append(r"C:\Program Files\QGIS 3.34.12\apps\qgis-ltr\python\plugins")     # Windows
sys.path.append('/usr/share/qgis/python/plugins')                                   # Ubuntu
import processing
from processing.core.Processing import Processing


class ProcessFeeback(QgsProcessingFeedback):
    def __init__(self):
        super().__init__()
        self.messages = []
        self.progress = 0

    def setProgress(self, progress):
        self.progress = progress
        self.messages.append(f'Progress: {progress}%')

    def reportError(self, msg, fatalError=False):
        self.messages.append(f'Error: {msg}')



def run_isochrone(start_loc, time_limit):
    
    # Supply path to qgis install location
    #qgis_path = r"C:\Program Files\QGIS 3.34.12\apps\qgis-ltr"     # Windows path
    qgis_path = '/usr'                                              # Ubuntu path
    QgsApplication.setPrefixPath(qgis_path, True)

    os.environ["PROJ_LIB"] = "/usr/share/proj"                      # Point to correct proj location (?)

    os.environ["QT_QPA_PLATFORM"] = "offscreen"                     # Flag QT to be offscreen/headless
    qgis = QgsApplication([], False)                                # Ref to QGIS app, set to no GUI

    project_path = '/portfolio_app/processing/TransitIsochroneTool/TransitConnectivity.qgs'
    project = QgsProject.instance()

    # Initialize a QGIS instance
    qgis.initQgis()
    
    project.read(project_path)    

    from AlgorithmProvider import AlgorithmProvider                 # Load algorithm provider only after reading in project
    Processing.initialize()
    provider = AlgorithmProvider()
    QgsApplication.processingRegistry().addProvider(provider)

    current_time = datetime.now().strftime("%Y-%m-%d--%H*%M*%S")

    params = {
            'STARTLOCATION'     : start_loc,
            'SEARCHTIMELIMIT'   : time_limit,
            'TIMESTAMP'         : current_time,
            'OUTPUT'            : 'TEMPORARY_OUTPUT'
            }

    context = QgsProcessingContext()
    context.setProject(project)

    feedback = ProcessFeeback()

    alg = QgsApplication.processingRegistry().algorithmById("alg_provider:transitservicearea")
    results = alg.run(params, context, feedback)                          

    QgsProject.instance().clear()
    qgis.exitQgis()
    del qgis
    return results[0]

if __name__ == "__main__":
    #print(sys.argv)
    run_isochrone(sys.argv[1], sys.argv[2])

# Test command line call:
# python3 ... '-13641659.399766,5697527.708063 [EPSG:3857]' 9