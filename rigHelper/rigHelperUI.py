import maya.cmds as cmds
import rigHelper.rigHelperLib as rhLib


class RigHelperUI():
    #Constructs UI
    def rigHelperUI(self, *args):
        #Checks if UI window exists
        windowName = 'RigHelper'
        if cmds.window(windowName, exists=True):
            cmds.deleteUI(windowName)

        cmds.window(windowName,w=200, h=300)
        cmds.columnLayout()
        cmds.button(l="Apply Default Rig", w=200, ann = "Applies the default character rig to the currently loaded model", c=self.applyRigPressed)
        
        cmds.showWindow(windowName)

    def applyRigPressed(self, *args):
        rhLib.redefineSkeleton()
        rhLib.applyRig()
        

rhelperUI = RigHelperUI()
rhelperUI.rigHelperUI()