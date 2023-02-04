import maya.cmds as cmds

def myFunction(*args):
    print("Button was pressed")

class RigHelperUI():
    #Constructs UI
    def rigHelperUI(self, *args):
        #Checks if UI window exists
        windowName = 'RigHelper'
        if cmds.window(windowName, exists=True):
            cmds.deleteUI(windowName)

        cmds.window(windowName,w=200, h=300)
        cmds.columnLayout()
        cmds.button(l="test", c="myFunction()")
        
        cmds.showWindow(windowName)
        

rhelperUI = RigHelperUI()
rhelperUI.rigHelperUI()