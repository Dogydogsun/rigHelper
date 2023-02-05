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
        cmds.button(l="Redefine Skeleton", w=200, ann = "Redefines the currently loaded character skeleton", c=self.redefineSkeletonPressed)
        cmds.button(l="Test", w=200, ann = "Test", c=self.myFunction)
        
        cmds.showWindow(windowName)

    def redefineSkeletonPressed(self, *args):
        rhLib.redefineSkeleton()

    def myFunction(self, *args):
        print("Test")
        

rhelperUI = RigHelperUI()
rhelperUI.rigHelperUI()