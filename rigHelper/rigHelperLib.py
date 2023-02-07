import maya.cmds as cmds
import os

class ErrorUI():
    def __init__(self, errorText = "Error", windowName = "Error"):
        self.errorText = errorText
        self.windowName = windowName
        self.errorUI()

    #Constructs UI
    def errorUI(self, *args):
        #Checks if UI window exists
        if cmds.window(self.windowName, exists=True):
            cmds.deleteUI(self.windowName)

        cmds.window(self.windowName,w=200, h=200)
        cmds.columnLayout()
        cmds.text(l=self.errorText, w=400, h=40, al="left", ww=True)
        cmds.button(l="Close", w=100, c=self.closeWindow)
        cmds.showWindow(self.windowName)

    def closeWindow(self, *args):
        cmds.deleteUI(self.windowName)

def prepareExport():
    allModels = cmds.listRelatives("models_GRP", ad=True)
    allJoints = cmds.listRelatives("joints_GRP", ad=True)
    cmds.select(allModels,allJoints)


def applyRig(rigPath):
    rigString = rigPath
    #Finds skeletal mesh in scene
    meshInScene = cmds.ls(type="mesh")
    for obj in meshInScene:
        if(obj.startswith("SK_")==True):
            skMesh = cmds.listRelatives(obj,type='transform',p=True)

    dirname = os.path.dirname(__file__)
    filename = dirname + rigString

    cmds.file(filename, reference = True, dns = True)

    intPrefix = "intermediate_"
    intermediateRoot = "intermediate_root_JNT"
    intermediateRootDescendants = cmds.listRelatives(intermediateRoot, allDescendents = True)
    intermediateJoints = [intermediateRoot]
    for child in intermediateRootDescendants:
        if cmds.objectType(child, isType = "joint"):
            intermediateJoints.append(child)
    print(intermediateJoints)
    for intjnt in intermediateJoints:
        jnt = intjnt[len(intPrefix):]
        cmds.parentConstraint(intjnt, jnt, mo=True, weight = 1)

    cmds.parent(skMesh, "models_GRP")
    cmds.parent("root_JNT", "joints_GRP")

    cmds.select(cl=True)


def redefineSkeleton():
    cmds.select(cl=True)
    obj = ""
    skMesh = []

    cmds.currentTime(0)

    #Finds skeletal mesh in scene
    meshInScene = cmds.ls(type="mesh")
    for obj in meshInScene:
        if(obj.startswith("SK_")==True):
            skMesh = cmds.listRelatives(obj,type='transform',p=True)


    def deleteKeyframes(object = ""):
        keyframes = []
        try:
            keyframes += cmds.listConnections(object,s=True, type="animCurveTU")
        except:
            pass
        try:
            keyframes += cmds.listConnections(object,s=True, type="animCurveTL")
        except:
            pass
        try:
            keyframes += cmds.listConnections(object,s=True, type="animCurveTA")
        except:
            pass
        
        cmds.delete(keyframes)


    def cleanAnim():
        try:
            allJoints = cmds.listRelatives("Root", ad = True)
        except:
            ErrorUI(errorText = "No group named 'Root' was found, please make sure this skeleton hasn't already been redefined.")
            cmds.error("No group named 'Root' was found, please make sure this skeleton hasn't already been redefined.")
        for jnt in allJoints:
            deleteKeyframes(jnt)


    def renameJoints():
        allJoints = cmds.listRelatives("Root", ad = True)
        
        for child in allJoints:
            if child.endswith('_l') or child.endswith('_L'):
                camelCase = child[0].lower() + child[1:]
                newName = "L_" + camelCase[:-2] + "_JNT"
                cmds.rename(child, newName)
            elif child.endswith('_r') or child.endswith('_R'):
                camelCase = child[0].lower() + child[1:]
                newName = "R_" + camelCase[:-2] + "_JNT"
                cmds.rename(child, newName)
            else:
                camelCase = child[0].lower() + child[1:]
                newName = "C_" + camelCase + "_JNT"
                cmds.rename(child, newName)


    def orgRig():
        cmds.joint(name="root_JNT",p=[0,0,0])
        cmds.parent("Root|C_pelvis_JNT", "root_JNT")
        cmds.delete("Root")


    def createSKMeshWeights():
        try:
            skMeshWeights = cmds.duplicate(skMesh, rr = True, un = True, name = "skMeshWeights")
        except:
            ErrorUI(errorText = "No character skeletal mesh found. Please check that the character mesh starts with the prefix SK_")
            cmds.error("No character skeletal mesh found. Please check that the character mesh starts with the prefix SK_")


    def adjustSkeleton():
        cmds.delete("|root_JNT|C_pelvis_JNT|C_spine_01_JNT|C_spine_02_JNT|C_spine_03_JNT|R_clavicle_JNT","|root_JNT|C_pelvis_JNT|R_thigh_JNT")
        
        cmds.select("|root_JNT|C_pelvis_JNT|C_spine_01_JNT|C_spine_02_JNT|C_spine_03_JNT|L_clavicle_JNT")
        cmds.mirrorJoint(mirrorYZ = True, mirrorBehavior = True, searchReplace = ["L_", "R_"])
        cmds.select(cl=True)
        
        cmds.select("|root_JNT|C_pelvis_JNT|L_thigh_JNT")
        cmds.mirrorJoint(mirrorYZ = True, mirrorBehavior = True, searchReplace = ["L_", "R_"])
        cmds.select(cl=True)
        
        
        cmds.delete("|root_JNT|C_pelvis_JNT|C_spine_01_JNT|C_spine_02_JNT|C_spine_03_JNT|L_clavicle_JNT","|root_JNT|C_pelvis_JNT|L_thigh_JNT")
        
        cmds.select("|root_JNT|C_pelvis_JNT|C_spine_01_JNT|C_spine_02_JNT|C_spine_03_JNT|R_clavicle_JNT")
        cmds.mirrorJoint(mirrorYZ = True, mirrorBehavior = True, searchReplace = ["R_", "L_"])
        cmds.select(cl=True)
        
        cmds.select("|root_JNT|C_pelvis_JNT|R_thigh_JNT")
        cmds.mirrorJoint(mirrorYZ = True, mirrorBehavior = True, searchReplace = ["R_", "L_"])
        cmds.select(cl=True)
        
        
        cmds.joint(name="C_center_JNT",p=[0,87.628,0])
        cmds.parent("C_center_JNT", "root_JNT")
        cmds.parent("|root_JNT|C_pelvis_JNT|R_thigh_JNT", "|root_JNT|C_center_JNT")
        cmds.parent("|root_JNT|C_pelvis_JNT|L_thigh_JNT", "|root_JNT|C_center_JNT")
        cmds.parent("|root_JNT|C_pelvis_JNT|C_spine_01_JNT", "|root_JNT|C_center_JNT")
        
        
        spine = ["|root_JNT|C_pelvis_JNT", "|root_JNT|C_center_JNT|C_spine_01_JNT", "|root_JNT|C_center_JNT|C_spine_01_JNT|C_spine_02_JNT", "|root_JNT|C_center_JNT|C_spine_01_JNT|C_spine_02_JNT|C_spine_03_JNT", "|root_JNT|C_center_JNT|C_spine_01_JNT|C_spine_02_JNT|C_spine_03_JNT|C_neck_01_JNT", "|root_JNT|C_center_JNT|C_spine_01_JNT|C_spine_02_JNT|C_spine_03_JNT", "|root_JNT|C_center_JNT|C_spine_01_JNT|C_spine_02_JNT|C_spine_03_JNT|C_neck_01_JNT|C_head_JNT"]
        
        for jnt in spine:
            childrenTmp=[]
            children = cmds.listRelatives(jnt, c = True, f = True)
            print(children)
            if children:
                for child in children:
                    cmds.select(child)
                    cmds.parent(child, w = True)
                    childrenTmp.append(cmds.ls(sl=True)[0])
                    cmds.select(cl = True)
                
            cmds.setAttr(jnt + ".rotateAxisX",0)
            cmds.setAttr(jnt + ".rotateAxisY",0)
            cmds.setAttr(jnt + ".rotateAxisZ",0)
            cmds.setAttr(jnt + ".jointOrientY",0)
            cmds.setAttr(jnt + ".jointOrientZ",0)
            if jnt is "|root_JNT|C_center_JNT|C_spine_01_JNT|C_spine_02_JNT|C_spine_03_JNT|C_neck_01_JNT|C_head_JNT":
                cmds.setAttr(jnt + ".jointOrientX",-30)
            for child in childrenTmp:
                cmds.parent(child, jnt)
            
            cmds.select(cl = True)
            
        
        cmds.parent("|root_JNT|C_center_JNT|C_spine_01_JNT|C_spine_02_JNT|C_spine_03_JNT|L_clavicle_JNT|L_upperArm_JNT", "|root_JNT|C_center_JNT|C_spine_01_JNT|C_spine_02_JNT|C_spine_03_JNT")
        cmds.parent("|root_JNT|C_center_JNT|C_spine_01_JNT|C_spine_02_JNT|C_spine_03_JNT|R_clavicle_JNT|R_upperArm_JNT", "|root_JNT|C_center_JNT|C_spine_01_JNT|C_spine_02_JNT|C_spine_03_JNT")
        
        cmds.setAttr("|root_JNT|C_pelvis_JNT.rotateAxisX",0)
        cmds.setAttr("|root_JNT|C_pelvis_JNT.rotateAxisY",0)
        cmds.setAttr("|root_JNT|C_pelvis_JNT.rotateAxisZ",0)
        cmds.parent("|root_JNT|C_pelvis_JNT", "|root_JNT|C_center_JNT")
        

    def removeSkin():
        cmds.skinCluster(skMesh, e=True, ub=True)


    #Reapplies skinning
    def reapplySkin():
        cmds.skinCluster(skMesh,"|root_JNT|C_center_JNT",name="skinCluster1")
        cmds.select("skMeshWeights", skMesh[0])
        cmds.copySkinWeights(noMirror = True, surfaceAssociation = "closestPoint", influenceAssociation = "name", normalize = True)
        cmds.delete("Root1","skMeshWeights")
        cmds.select(cl=True)


    cleanAnim()
    renameJoints()
    createSKMeshWeights()
    orgRig()
    removeSkin()
    adjustSkeleton()
    reapplySkin()