import maya.cmds as cmds
import rigHelper.rigHelperLib as rhLib


class RigHelperUI():
    #Constructs UI
    def rigHelperUI(self, *args):
        #Checks if UI window exists
        windowName = 'RigHelper'
        if cmds.window(windowName, exists=True):
            cmds.deleteUI(windowName)

        cmds.window(windowName,w=200, h=100)
        cmds.columnLayout()
        cmds.button(l="Apply Dwarf Rig", w=200, ann = "Applies the default dwarf character rig to the currently loaded model", c=self.applyRigPressed)
        cmds.button(l="Apply Human Rig", w=200, ann = "Applies the default Human character rig to the currently loaded model", c=self.applyHumanRigPressed)
        cmds.button(l="Prepare For Export", w=200, ann = "Selects all necesarry objects for game export", c=self.prepareExportPressed)
        
        cmds.showWindow(windowName)

    def applyRigPressed(self, *args):
        rhLib.redefineSkeleton()
        rhLib.applyRig(rigPath = r'\rigs\rigHelper_dwarf_defaultRig.ma')

    def applyHumanRigPressed(self, *args):
        rhLib.redefineSkeleton()
        rhLib.applyRig(rigPath = r'\rigs\rigHelper_human_defaultRig.ma')

    def prepareExportPressed(self, *args):
        rhLib.prepareExport()

        

rhelperUI = RigHelperUI()
rhelperUI.rigHelperUI()