Welcome to rigHelper. A small package for Maya to help import custom rigs for characters.

Currently only meant to function for specific character in a private project.


To install, download the latest release from the Github Releases tab.
Unzip the folder and place the "rigHelper" folder in any unrestricted location on your PC.

To run the package, paste the following code into the Maya script editor:

import sys
import importlib

#!Input path to rigHelper package directory here!
packPath = r"D:/Projects/rigHelper"

try:
    if rigHelperLoaded == True:
        importlib.reload(rigHelper)
except:
    sys.path.append(packPath)
    rigHelperLoaded = True
    import rigHelper


Remember to fill the complete path to where you placed the package in the "packPath" field between the quotation marks. 

---------------------------------------------------------------------------------------------------------

rigHelper should now succesfully run in your instance of Maya. It is recommended that you make the previous script a custom shelf button by selecting the entire script in the Maya script editor, and middle-mouse dragging it onto the Maya shelf.


Currently 2 different rigs are provided with rigHelper, human and dwarf. To load your choice simply click the corresponding button in the window that appears
when the package is loaded. When loading a rig. Make sure that you scene is completely empty except for the character which you wish to apply the rig to.
If you wish to have multiple characters in the same scene, first apply the rigs in seperate scenes, save the new character rigs, and reference them into a new scene.


You can use the rigHelper to help prepare the rig for export.
Click the "Prepare for Export" button, and all necesarry parts of the rig will be selected and you can now export your animations.
