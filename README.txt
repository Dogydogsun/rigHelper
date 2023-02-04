To start the plugin, run the following in the Maya script editor


import sys
import importlib

#Input path to autorig package directory here
packPath = 'D:/Projects/Repositories/rigHelper'

try:
    if rigHelperLoaded == True:
        importlib.reload(rigHelper)
except:
    sys.path.append(packPath)
    rigHelperLoaded = True
    import rigHelper
