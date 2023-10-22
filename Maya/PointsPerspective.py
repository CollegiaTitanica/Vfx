import maya.cmds as mc
import maya.app.renderSetup.model.renderSetup as renderSetup
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import sys, importlib


sys.path.append(r"\\fs3\Sh1\uber\Master\MayaScripts_2018\include_scripts")
import camera_btn_Qt, space_change
importlib.reload(camera_btn_Qt)
importlib.reload(space_change)

###
global Original_BackGround

global Original_BG_R
global Original_BG_G
global Original_BG_B


global Original_BackGroundTOP
global Original_BGT_R
global Original_BGT_G
global Original_BGT_B


global Original_BackGroundBOTTOM

global Original_BGB_R
global Original_BGB_G
global Original_BGB_B



class CameraStabilizera(object):
    global activeCam, activeCamShape


    def CS_ON(self):
        cmds.expression(n="CameraStabilizer", s='python("setOffset()");')
        #self.setOffset2()
        sys.stdout.write("Camera Stabilizer Mode ON")


    def CS_OFF(self):
        global activeCam, activeCamShape
        try:
            cmds.delete("CameraStabilizer")
        except:
            pass

        cmds.setAttr(activeCamShape + ".horizontalFilmOffset", 0)  # reset Camera Offset after exiting Stabilizing mode
        cmds.setAttr(activeCamShape + ".verticalFilmOffset", 0)
        cmds.setAttr(activeCamShape + ".panZoomEnabled", 0)  # 2d pan off

        sys.stdout.write("Camera Stabilizer Mode OFF")


    def setOffset2(self):
        # UNDO OFF
        cmds.undoInfo(swf=1)

        # Conditions
        cs_stab_obj_exists = False
        if cmds.objExists(cs_stab_obj) or (cs_stab_obj == ''):
            cs_stab_obj_exists = True
        else:
            cmds.warning(cs_stab_obj + ' does not exist!')
        try:
            sel = cmds.ls(sl=1)[0]
            sel_shape = cmds.listRelatives(sel, c=1)
            sel_shape_type = cmds.nodeType(sel_shape)

        except:
            sel_shape_type = "None"
        #    cmds.warning('wrong selection!')


        if cmds.ls(sl=1) and (sel_shape_type != 'camera') and cs_stab_obj_exists:

            if cs_stab_obj == '':
                locator = cmds.ls(sl=1)[0]  # get first selected object
            else:
                locator = cs_stab_obj

            # 2d padding
            cmds.setAttr(activeCamShape + ".panZoomEnabled", 1)
            cmds.setAttr(activeCamShape + ".horizontalPan", 0)
            cmds.setAttr(activeCamShape + ".verticalPan", 0)
            #cmds.setAttr(activeCamShape + ".zoom", 0.3)

            oldOffsetX = cmds.getAttr(activeCamShape + ".horizontalFilmOffset")  # old Film OffsetX
            oldOffsetY = cmds.getAttr(activeCamShape + ".verticalFilmOffset")  # old Film OffsetY

            x = cmds.xform(locator, q=1, ws=1, rp=1)[0]
            y = cmds.xform(locator, q=1, ws=1, rp=1)[1]  # world position for locator (x,y,z)
            z = cmds.xform(locator, q=1, ws=1, rp=1)[2]

            ptx = space_change.worldToScreen(activeCam, (x, y, z), (1, -1))[0]  # worldSpace to CameraSpace (x,y)
            pty = space_change.worldToScreen(activeCam, (x, y, z), (1, -1))[1]

            ptx = ((ptx/2)+0.5) * (-1)
            pty = (pty/2) + 0.5

            rangeX = ((cmds.getAttr(activeCamShape + ".horizontalFilmAperture")) / 2)  # width of half screen in inches
            rangeY = ((cmds.getAttr(activeCamShape + ".verticalFilmAperture")) / 2)  # height of half screen in inches

            OffsetX = oldOffsetX - (ptx * rangeX*2 + rangeX)
            OffsetY = oldOffsetY - (pty * rangeY*2 - rangeY)

            cmds.setAttr(activeCamShape + ".horizontalFilmOffset", OffsetX)  # set new Film Offset
            cmds.setAttr(activeCamShape + ".verticalFilmOffset", OffsetY)


    # UNDO ON
    cmds.undoInfo(swf=True)
    # -------------------

        # -------------------
    def CheckCameraStabilizer(self):

    #    if cmds.objExists('CameraStabilizer'):
    #        self.CS_OFF()

        # if there is only 1 camera
        #elif len(cmds.listCameras()) == 5:
        if len(cmds.listCameras()) == 5:
            for i in cmds.listCameras():
                if i != 'front' and i != 'persp' and i != 'side' and i != 'top':
                    activeCam = i

            activeCamShape = cmds.listRelatives(activeCam, c=True)[0]
            self.CS_ON()

        # if there is more than 1 camera
        else:

            # UI
            Win_CS = QWidget()

            vbox = QVBoxLayout(Win_CS)

            def click():
                Win_CS.close()
                if not cmds.objExists('CameraStabilizer'):
                    self.CS_ON()
                else:
                    self.CS_OFF()

        #    exec(camera_btn_Qt.exec_addCamButtons('cs'))
            camera_btn_Qt.exec_addCamButtons('cs')

            Win_CS.setLayout(vbox)

            Win_CS.setGeometry((1920 / 2) - (400 / 2), (1080 / 2) - (100 / 2), 400, 100)
            Win_CS.setWindowTitle('Camera Stabilizer')
            Win_CS.setWindowIcon(QIcon(BASE_DIR + 'vertigo_shelf/icons/VV.png'))
            Win_CS.setWindowFlags(Qt.WindowStaysOnTopHint)
            Win_CS.show()

def Write_Perspective_Attributes():


    sCam=mc.ls('persp')
    print ("sCam = {}".format(sCam))
    sCS = mc.listRelatives(sCam, c=1)
    print ("sCS = {}".format(sCS))


    attributes = mc.listAttr(sCam,keyable=True)
    attributesShape = mc.listAttr(sCS,keyable=True,visible=True)

    print ("attributes = {}".format(attributes))
    print ("attributesShape = {}".format(attributesShape))
 
    with open (Perspective_Attributes_File,"w") as file:
    #   Focal = "FocalLength={}".format(FL)
        
        for attr in attributes:
            AttributeValue = mc.getAttr(sCam[0]+".{}".format(attr))
            attributeLine = "{} = {}".format(attr,AttributeValue)
            print (attributeLine)
            file.writelines(attributeLine + "\n")
        
        for attrShape in attributesShape:
            try:
                AttributeShapeValue = mc.getAttr(sCS[0]+".{}".format(attrShape))
            except RuntimeError:
                pass
            attributeShapeLine = "{} = {}".format(attrShape,AttributeShapeValue)
            print (attributeShapeLine)
            file.writelines(attributeShapeLine + "\n")

def Reset_Perspective():
    sCam=mc.ls('persp')
    print ("sCam = {}".format(sCam))
    sCS = mc.listRelatives(sCam, c=1)
    print ("sCS = {}".format(sCS))

    with open(Perspective_Attributes_File) as RL:
        Perspective_Attr_Text = RL.readlines()
        for line in Perspective_Attr_Text: 
            attribute = line.split("=")[0]
            value = line.split("=")[1]
            
            try:
                value = float(value)
            except ValueError:
                try:
                    value = bool(value)
                except ValueError():
                    pass


            print ("attribute = {}".format(attribute))
            print ("Typeattribute = {}".format(type(attribute)))
            print ("value = {}".format(value))
            print ("TypeValue = {}".format(type(value)))

            try:
                mc.setAttr(sCam[0] +".{}".format(attribute), value)
                print ("Attribute PASSED = {}".format(attribute))
            except RuntimeError:
                print ("Attribute FAILED = {}".format(attribute))
                pass



def FindMayaVersion():
    MayaName = mc.file(q=True,sn=True,shn=True)
    SplitMayaName = MayaName.split("_")
    print ("SplitMayaName = {}".format(SplitMayaName))
    for q in reversed(SplitMayaName):
        if "v00" in q:
            return (q)

def CleanUp():
    rs = renderSetup.instance()
    rs.clearAll()
    master= rs.getDefaultRenderLayer()
    master.setRenderable(False)
    layers= mc.ls(long=True,type="displayLayer")
    for layer in layers:
        if "Locators" or "Cones_Mesh" or "RestOfGeo" in layer and "defaultLayer" not in layer:
            mc.delete(layer)
def CleanUp2():
    rs = renderSetup.instance()
    rs.clearAll()
    master= rs.getDefaultRenderLayer()
    master.setRenderable(False)
    layers= mc.ls(long=True,type="displayLayer")
    for layer in layers:
        if "defaultLayer" not in layer:
            mc.delete(layer)

def LockPerspective(LOCK=False):
    #Lock Perspective Camera
    SelectedCamera=mc.ls('persp')
    mc.setAttr(SelectedCamera[0] +".tx", lock=LOCK)
    mc.setAttr(SelectedCamera[0] +".ty", lock=LOCK)
    mc.setAttr(SelectedCamera[0] +".tz", lock=LOCK)
    mc.setAttr(SelectedCamera[0] +".rx", lock=LOCK)
    mc.setAttr(SelectedCamera[0] +".ry", lock=LOCK)
    mc.setAttr(SelectedCamera[0] +".rz", lock=LOCK)

    mc.setAttr(SelectedCamera[0] +".hfa", lock=LOCK)
    mc.setAttr(SelectedCamera[0] +".vfa", lock=LOCK)
    mc.setAttr(SelectedCamera[0] +".fl", lock=LOCK)
    mc.setAttr(SelectedCamera[0] +".lsr", lock=LOCK)
    mc.setAttr(SelectedCamera[0] +".fs", lock=LOCK)
    mc.setAttr(SelectedCamera[0] +".sa", lock=LOCK)
    mc.setAttr(SelectedCamera[0] +".fd", lock=LOCK)
    mc.setAttr(SelectedCamera[0] +".coi", lock=LOCK)
    mc.setAttr(SelectedCamera[0] +".lls", lock=LOCK)


def Points_PerspectiveWindow():
    LockPerspective(LOCK=False)
    global lidar
    global Points_PerspectiveWindow
    global Perspective_Attributes_File

    FullMayaPath = mc.file(q=True,sn=True)
    MayaFolder = FullMayaPath.split("/")

    for j in MayaFolder[::-1]:
        MayaFolder.remove(j)
        if j == "main3d":
            break

    MayaFolder = "/".join(MayaFolder)
    MayaFolder= MayaFolder + "/main3d"

    print ("MayaFolder = {}".format(MayaFolder))
    Perspective_Attributes_File = MayaFolder + "/Perspective_Attributes.txt" 

    lidar = 0
    mc.setAttr('defaultRenderGlobals.currentRenderer', 'mayaHardware2', type='string')
    mc.setAttr ("hardwareRenderingGlobals.lineAAEnable", 0)
    mc.setAttr ("hardwareRenderingGlobals.lineAAEnable", 1)
    mc.setAttr ("hardwareRenderingGlobals.multiSampleEnable", 0)
    mc.setAttr ("hardwareRenderingGlobals.multiSampleEnable", 1)
    mc.setAttr ("hardwareRenderingGlobals.ssaoEnable", 0)
    mc.setAttr ("hardwareRenderingGlobals.lightingMode", 0)
    mc.setAttr ("hardwareRenderingGlobals.renderMode", 5)
    mc.setAttr ("defaultRenderGlobals.imageFormat",8)
    
    Points_PerspectiveWindow = mc.window( title="Render Settings", iconName='RS', w=(600), h=100 )
    mc.columnLayout( adjustableColumn=True )
    mc.text(label='Time to Choose Mr. Freeman',w=200, h=100,rs=1)
    mc.rowLayout(nc=2)
    mc.button(w=300, h=50, label='PointsLidar', command=('Points_Window()') )
    mc.button(w=300, h=50, label='Perspective', command=('Perspective_Window()' ))
    mc.setParent( '..' )
    mc.showWindow( Points_PerspectiveWindow )

def Points_Window():
    global Points_Window

    global Original_BackGround

    global Original_BG_R
    global Original_BG_G
    global Original_BG_B


    global Original_BackGroundTOP
    global Original_BGT_R
    global Original_BGT_G
    global Original_BGT_B


    global Original_BackGroundBOTTOM

    global Original_BGB_R
    global Original_BGB_G
    global Original_BGB_B
    
    mc.modelEditor('modelPanel4' , edit = True, lw=4)
    mc.modelEditor('modelPanel4' , edit = True,displayAppearance='smoothShaded',wireframeOnShaded=True,nurbsCurves=False,locators=True,cameras=True,imagePlane=True)
    Points_Window   = mc.window( title="PointsLidar Setup", iconName='Camera', w=(300), h=100 )
    mc.columnLayout( adjustableColumn=True )
    mc.text(label='Select the Locator/Cone that you want to stabilize to',w=200, h=100,rs=1)
    mc.rowLayout(nc=1)

    ProceedButton = mc.button(w=300, h=50, label='Proceed',align='center', command=('Proceed_PointsLidar()') ,backgroundColor=(0.43,0.58,1.0))
    mc.setParent( '..' )
### Holdout
    HoldoutGeo= mc.listRelatives(mc.ls(type='mesh'), p = True, f = True)
    for geo in HoldoutGeo:
    
        mc.setAttr(geo +".holdOut",1)
    
    mc.select(clear=True)
###
    RestOfGeo= mc.listRelatives(mc.ls(type='mesh'), p = True, f = True)

    mc.select(RestOfGeo)
    DisplayRestOfGeo = mc.createDisplayLayer (name= "RestOfGeo" ,nr=1)
    mc.setAttr("{}.displayType".format(DisplayRestOfGeo),2)
    mc.select(clear=True)

    mc.showWindow(Points_Window) 
    mc.deleteUI( Points_PerspectiveWindow, window=True )
########  BackGround Color
   # Original_BackGround =mc.displayRGBColor('background',q=True)    #[0.6309999823570251, 0.6309999823570251, 0.6309999823570251]
    Original_BackGround = [0.6309999823570251, 0.6309999823570251, 0.6309999823570251]
    print ("Original_BackGround = {}".format(Original_BackGround))
    Original_BG_R = Original_BackGround[0]
    Original_BG_G = Original_BackGround[1]
    Original_BG_B = Original_BackGround[2]
    mc.displayRGBColor('background',0,0,0)
    


   # Original_BackGroundTOP =mc.displayRGBColor('backgroundTop',q=True)  #[0.5350000262260437, 0.6169999837875366, 0.7020000219345093]
    Original_BackGroundTOP = [0.5350000262260437, 0.6169999837875366, 0.7020000219345093]
    print ("Original_BackGroundTOP = {}".format(Original_BackGroundTOP))
    Original_BGT_R = Original_BackGroundTOP[0]
    Original_BGT_G = Original_BackGroundTOP[1]
    Original_BGT_B = Original_BackGroundTOP[2]
    mc.displayRGBColor('backgroundTop',0,0,0)
    


   # Original_BackGroundBOTTOM =mc.displayRGBColor('backgroundBottom',q=True) # [0.052000001072883606, 0.052000001072883606, 0.052000001072883606]
    Original_BackGroundBOTTOM =  [0.052000001072883606, 0.052000001072883606, 0.052000001072883606]
    print ("Original_BackGroundBOTTOM = {}".format(Original_BackGroundBOTTOM))
    Original_BGB_R = Original_BackGroundBOTTOM[0]
    Original_BGB_G = Original_BackGroundBOTTOM[1]
    Original_BGB_B = Original_BackGroundBOTTOM[2]
    mc.displayRGBColor('backgroundBottom',0,0,0)


    CameraObject = CameraStabilizera()
    CameraObject.CS_ON()


def Perspective_Window():
    global Perspective_Window
    global Selected_Camera
    global Original_BackGround

    global Original_BG_R
    global Original_BG_G
    global Original_BG_B


    global Original_BackGroundTOP
    global Original_BGT_R
    global Original_BGT_G
    global Original_BGT_B


    global Original_BackGroundBOTTOM

    global Original_BGB_R
    global Original_BGB_G
    global Original_BGB_B


    Perspective_Window   = mc.window( title="Perspective Setup", iconName='Camera', w=(300), h=100 )
    mc.columnLayout( adjustableColumn=True )
    mc.text(label='Adjust the view that you wish to render a perspective of',w=200, h=100,rs=1)
    mc.rowLayout(nc=1)

    ### Holdout
    HoldoutGeo= mc.listRelatives(mc.ls(type='mesh'), p = True, f = True)
    for geo in HoldoutGeo:
    
        mc.setAttr(geo +".holdOut",0)
    
    mc.select(clear=True)
    mc.modelEditor('modelPanel4' , edit = True,displayAppearance='smoothShaded',wireframeOnShaded=False,nurbsCurves=False,motionTrails=True,polymeshes=True,locators=True,cameras=True,selectionHiliteDisplay=True)
###
    

########  BackGround Color
   # Original_BackGround =mc.displayRGBColor('background',q=True)    #[0.6309999823570251, 0.6309999823570251, 0.6309999823570251]
    Original_BackGround = [0.6309999823570251, 0.6309999823570251, 0.6309999823570251]
    print ("Original_BackGround = {}".format(Original_BackGround))
    Original_BG_R = Original_BackGround[0]
    Original_BG_G = Original_BackGround[1]
    Original_BG_B = Original_BackGround[2]
    mc.displayRGBColor('backgroundBottom',0.36,0.36,0.36)
    


   # Original_BackGroundTOP =mc.displayRGBColor('backgroundTop',q=True)  #[0.5350000262260437, 0.6169999837875366, 0.7020000219345093]
    Original_BackGroundTOP = [0.5350000262260437, 0.6169999837875366, 0.7020000219345093]
    print ("Original_BackGroundTOP = {}".format(Original_BackGroundTOP))
    Original_BGT_R = Original_BackGroundTOP[0]
    Original_BGT_G = Original_BackGroundTOP[1]
    Original_BGT_B = Original_BackGroundTOP[2]
    mc.displayRGBColor('backgroundBottom',0.36,0.36,0.36)
    


   # Original_BackGroundBOTTOM =mc.displayRGBColor('backgroundBottom',q=True) # [0.052000001072883606, 0.052000001072883606, 0.052000001072883606]
    Original_BackGroundBOTTOM =  [0.052000001072883606, 0.052000001072883606, 0.052000001072883606]
    print ("Original_BackGroundBOTTOM = {}".format(Original_BackGroundBOTTOM))
    Original_BGB_R = Original_BackGroundBOTTOM[0]
    Original_BGB_G = Original_BackGroundBOTTOM[1]
    Original_BGB_B = Original_BackGroundBOTTOM[2]
    mc.displayRGBColor('backgroundBottom',0.36,0.36,0.36)
    


######## Write Perspective Camera Coordinates if version is v001, else reset to coordinates
    global Version
    Version = FindMayaVersion()
    if Version != "v001".lower():
       # try:
        Reset_Perspective()
        LockPerspective(LOCK=True)
        #except:
        #    print("Coordinates not found")
        #    pass
####
    CleanUp()
    locators = mc.listRelatives(mc.ls(type='locator'),p = True, f = True)
    mc.select(locators)
    DisplayLocators = mc.createDisplayLayer (name= "Locators" ,nr=1)
    mc.setAttr("%s.visibility" %DisplayLocators,False)

    
####
    RestOfGeo= mc.listRelatives(mc.ls(type='mesh'), p = True, f = True)

    mc.select(RestOfGeo)
    DisplayRestOfGeo = mc.createDisplayLayer (name= "RestOfGeo" ,nr=1)
    mc.setAttr("{}.displayType".format(DisplayRestOfGeo),2)
    mc.select(clear=True)

###
    AllGeo= mc.listRelatives(mc.ls(type='mesh'), p = True, f = True) 
    ConesMesh = []
    for meshes in AllGeo:
        if "cone" in meshes:
            ConesMesh.append(meshes)

    print("ConesMesh = {}".format(ConesMesh))

    mc.select(ConesMesh)
    DisplayCones = mc.createDisplayLayer (name= "Cones_Mesh" ,nr=1)
    mc.setAttr("%s.visibility" %DisplayCones,False)
    mc.setAttr("{}.displayType".format(DisplayCones),2)
    mc.select(clear=True)
##  Turn off Nurbs Curves
    mc.modelEditor('modelPanel4' , edit = True,nurbsCurves=False)
##### CAMERA CHECK
    Camera=str(mc.lookThru(q=True))
    print ("Camera: {}".format(Camera)) 
    ListOfCameras=cmds.listCameras()
    ExcludeList = ['front', 'persp', 'side', 'top']
    NeededCamera = []

    if Camera in ExcludeList:
        for cam in ListOfCameras:
            if cam in ExcludeList:
                continue
            else:
                NeededCamera.append(cam)
        try:       
            Camera=NeededCamera[0]
            print(Camera)
        except:
            pass
    else:
        print("Kamera = {}".format(Camera))

#####
    
    mc.lookThru('persp')
    Selected_Camera = mc.ls('{}'.format(Camera))[0]
    print ("Selected_Camera: {}".format(Selected_Camera)) 
    mc.viewFit('persp','{}'.format(Selected_Camera))
    mc.modelEditor('modelPanel4' , edit = True,displayAppearance='smoothShaded')
    mc.select(Selected_Camera)
    #PerspectiveCamera(Camera)
    startF = int(mc.playbackOptions(min=True, q=True))
    endF = int(mc.playbackOptions(max=True, q=True))
    # Delete Motion Trails
    trails = mc.listRelatives(mc.ls(type='motionTrailShape'), p = True, f = True) 
    mc.delete(trails)
    mc.snapshot("{}".format(Selected_Camera),startTime=startF,endTime=endF,motionTrail=True,name="MotionTrail")
   # Naem = mc.snapshot("{Selected_Camera}".format(Selected_Camera),q=True,startTime=startF,endTime=endF,motionTrail=True,name="MotionTrail")
   # print("Naem = {}".format(Naem))

    ProceedButton = mc.button(w=300, h=50, label='Proceed',align='center', command=('Proceed_Perspective()') ,backgroundColor=(1.0,0.49,0.15))
    mc.setParent( '..' )
    mc.showWindow(Perspective_Window) 
    mc.deleteUI( Points_PerspectiveWindow, window=True )


def Proceed_PointsLidar():
    global Selected_Camera
    CleanUp()
    PointsLidarPath = r"\\fs3\TPN\ImageEngine\SNP4\render\SNP4_405-066_SNP4-405-066-005_bg_native_v0001\TEST\\" + "ShotName"
    ####
    IE_ShotID,ActualRenderFolder,IEVersion=Get_ShotName("pointsLidar")
    print ("NEW_IE_ShotID: {}".format(IE_ShotID))
    print ("NEW_ActualRenderFolder: {}".format(ActualRenderFolder))
    print ("NEW_IEVersion: {}".format(IEVersion))
    ####
    

    LastSelection = mc.ls( dag=True, ap=True, sl=True )    

    AllGeo= mc.listRelatives(mc.ls(type='mesh'), p = True, f = True)
    mc.color( AllGeo, rgb=(0.000,0.001,0.117) ) 

    # Delete Motion Trails
    trails = mc.listRelatives(mc.ls(type='motionTrailShape'), p = True, f = True) 
    mc.delete(trails)

    locators = mc.listRelatives(mc.ls(type='locator'),p = True, f = True)

    print("locators = {}".format(locators))

    mc.select(locators)
    DisplayLocators = mc.createDisplayLayer (name= "Locators" ,nr=1)
    mc.setAttr("%s.visibility" %DisplayLocators,False)

    ConesMesh = []
    for meshes in AllGeo:
        if "cone" in meshes:
            ConesMesh.append(meshes)

    print("ConesMesh = {}".format(ConesMesh))

    mc.select(ConesMesh)
    DisplayCones = mc.createDisplayLayer (name= "Cones_Mesh" ,nr=1)
    mc.setAttr("%s.visibility" %DisplayCones,False)
    CameraObjecta = CameraStabilizera()
  #  CameraObjecta.CheckCameraStabilizer()
   # CameraObjecta.CS_ON()
   
    ##### CAMERA CHECK
    Camera=str(mc.lookThru(q=True))
    print ("Camera: {}".format(Camera)) 
    ListOfCameras=cmds.listCameras()
    ExcludeList = ['front', 'persp', 'side', 'top']
    NeededCamera = []

    if Camera in ExcludeList:
        for cam in ListOfCameras:
            if cam in ExcludeList:
                continue
            else:
                NeededCamera.append(cam)
        try:       
            Camera=NeededCamera[0]
            print(Camera)
        except:
            pass
    else:
        print("Kamera = {}".format(Camera))

#####
    
    Selected_Camera = mc.ls('{}'.format(Camera))[0]
    print ("Selected_Camera: {}".format(Selected_Camera))

    cam = Selected_Camera
    cam_shape = mc.listRelatives(cam, c=1)
    cam_image = mc.listRelatives(mc.listConnections(cam_shape[0]), c=True)
    MaxW = float((mc.getAttr(cam, cam_image[0] + ".coverageX")))    
    MaxH = float((mc.getAttr(cam, cam_image[0] + ".coverageY")))
    print ("MaxW: {}".format(MaxW))  
    print ("MaxH: {}".format(MaxH))
    mc.setAttr("defaultResolution.w", MaxW)
    mc.setAttr("defaultResolution.h", MaxH)

    #deselect the layer objects and reselect the Last selected Locator/Cone
    mc.select(clear=True)
    mc.select(LastSelection)
    def scene_resolution():
        return [mc.getAttr("defaultResolution.width"),mc.getAttr("defaultResolution.height")]

    mc.setAttr ("hardwareRenderingGlobals.multiSampleEnable", 1)

    ##############
    PointsLidarFolder = ActualRenderFolder
    PointsLidarName = PointsLidarFolder + IE_ShotID + "_pointsLidar_" + IEVersion
    print ("PointsLidarFolder: {}".format(PointsLidarFolder))
    print ("PointsLidarName: {}".format(PointsLidarName))
    if not os.path.exists(PointsLidarFolder):
        original_umask = os.umask(0)
        os.makedirs(PointsLidarFolder,mode=0o777  )
    ##############
    Resolution = scene_resolution()
    print(Resolution)
   # mc.modelEditor('modelPanel4' , edit = True, lw=4)
    #mc.playblast(widthHeight=(0,0),format="image",filename=PointsLidarName,percent=100,showOrnaments=False,viewer=False,forceOverwrite=True)
    mc.playblast(widthHeight=Resolution,format="image",filename=PointsLidarName,percent=100,showOrnaments=False,viewer=False,forceOverwrite=True)
    
    mc.modelEditor('modelPanel4' , edit = True, lw=1)

    CameraObjecta.CS_OFF()
    mc.setAttr ("hardwareRenderingGlobals.multiSampleEnable", 0)

    mc.modelEditor('modelPanel4' , edit = True,nurbsCurves=False)
    CleanUp2()
    mc.deleteUI( Points_Window, window=True )

    mc.displayRGBColor('background',Original_BG_R,Original_BG_G,Original_BG_B)
    mc.displayRGBColor('backgroundTop',Original_BGT_R,Original_BGT_G,Original_BGT_B)
    mc.displayRGBColor('backgroundBottom',Original_BGB_R,Original_BGB_G,Original_BGB_B)

#Proceed_PointsLidar()
Points_PerspectiveWindow()


def PerspectiveCamera(Camera):
    startF = int(mc.playbackOptions(min=True, q=True))
    endF = int(mc.playbackOptions(max=True, q=True))

    SelectedCamera=mc.ls('{}'.format(Camera))[0]
    mc.snapshot("{SelectedCamera}".format(SelectedCamera),startTime=startF,endTime=endF,motionTrail=True,name="MotionTrail")
    


def Napravi_Ga_Savku():
    FullMayaPath_No_ext = mc.file(q=True,sn=True)
    FullMayaPath_No_ext = FullMayaPath_No_ext.split(".")
    FullMayaPath_No_ext.pop()
    FullMayaPath_No_ext = "".join(FullMayaPath_No_ext)
    print("FullMayaPath_No_ext = {}".format(FullMayaPath_No_ext))

    PerspectiveMayaName = '{}'.format(FullMayaPath_No_ext) + "_Perspective" + ".ma"
    print("PerspectiveMayaName = {}".format(PerspectiveMayaName))
    MayaName = mc.file(q=True,sn=True,shn=True)
    print("MayaName = {}".format(MayaName))
    SplitMayaName = MayaName.split(".")
    SplitMayaName.pop()
    SplitMayaName = "".join(SplitMayaName)
    SplitMayaName = SplitMayaName.split("_")
    print("SplitMayaName = {}".format(SplitMayaName))
    LastSLOG = SplitMayaName[-1]
    if LastSLOG.lower() != "Perspective".lower():
        mc.file(rename=PerspectiveMayaName)
        mc.file(save=True,type='mayaAscii')

    elif LastSLOG.lower() == "Perspective".lower():
        mc.file(save=True,type='mayaAscii')    



def scene_resolution():
    return [mc.getAttr("defaultResolution.width"),mc.getAttr("defaultResolution.height")]

def scene_frameRange():
    startF = int(cmds.playbackOptions(min=True, q=True))
    endF = int(cmds.playbackOptions(max=True, q=True))
    return [startF,endF]

def Get_ShotName(Render_Perspective):
    FullMayaPath = mc.file(q=True,sn=True)
    ActualMayaPath = FullMayaPath.split("/")

    for j in ActualMayaPath[::-1]:
        ActualMayaPath.remove(j)
        if j == "main3d":
            break
    PreviewPath = ActualMayaPath
    for n, k in enumerate(PreviewPath):
        if k == "3d_comp":
            PreviewPath[n] = "render"

    ActualRenderFolder = "/".join(PreviewPath) + "/preview/" + "Render/" + "{}/".format(Render_Perspective)
    print ("ActualRenderFolder = {}".format(ActualRenderFolder))
    if not os.path.exists(ActualRenderFolder):
        original_umask = os.umask(0)
        os.makedirs(ActualRenderFolder,mode=0o777  )
    ShotName = ActualMayaPath[-1]
    print ("ShotName = {}".format(ShotName))
    IEVersion = ShotName.split("_")[-1]
    IE_ShotID = ShotName.split("_")[-4]
    IE_ShotID = "".join(IE_ShotID)

    IE_ShotID = IE_ShotID.split("-")
    print ("IE_ShotID = {}".format(IE_ShotID))

    Split_ID1 = IE_ShotID [:-2]
    Split_ID1= "_".join(Split_ID1)
    Split_ID2 = IE_ShotID [-2:]
    Split_ID2= "_".join(Split_ID2)
    print ("Split_ID1 = {}".format(Split_ID1))
    print ("Split_ID2 = {}".format(Split_ID2))
    Joined_ID = [Split_ID1,Split_ID2]
    IE_ShotID = "-".join(Joined_ID)
    print ("IE_ShotID = {}".format(IE_ShotID))
    
    return IE_ShotID,ActualRenderFolder,IEVersion

def Proceed_Perspective():
    ####
    IE_ShotID,ActualRenderFolder,IEVersion=Get_ShotName("perspective")
    print ("NEW_IE_ShotID: {}".format(IE_ShotID))
    print ("NEW_ActualRenderFolder: {}".format(ActualRenderFolder))
    print ("NEW_IEVersion: {}".format(IEVersion))
    ####
    cam = Selected_Camera
    cam_shape = mc.listRelatives(cam, c=1)
    cam_image = mc.listRelatives(mc.listConnections(cam_shape[0]), c=True)
    MaxW = float((mc.getAttr(cam, cam_image[0] + ".coverageX")))    
    MaxH = float((mc.getAttr(cam, cam_image[0] + ".coverageY")))
    print ("MaxW: {}".format(MaxW))  
    print ("MaxH: {}".format(MaxH))
    mc.setAttr("defaultResolution.w", MaxW)
    mc.setAttr("defaultResolution.h", MaxH)
    ####
   # PerspectiveFolder = r"\\fs3\TPN\ImageEngine\SNP4\render\SNP4_405-066_SNP4-405-066-005_bg_native_v0001\PERSPECTIVE\\"
    PerspectiveFolder = ActualRenderFolder
    PerspectiveName = PerspectiveFolder + IE_ShotID + "_perspective_" + IEVersion
    print ("PerspectiveFolder: {}".format(PerspectiveFolder))
    print ("PerspectiveName: {}".format(PerspectiveName))
    if not os.path.exists(PerspectiveFolder):
        original_umask = os.umask(0)
        os.makedirs(PerspectiveFolder,mode=0o777  )

    if Version == "v001".lower():
        Write_Perspective_Attributes()

    LockPerspective(LOCK=True)
    mc.deleteUI( Perspective_Window, window=True )

    mc.select(clear=True)
    mc.select(Selected_Camera)

    ### Empty preview folder
    for imagefile in os.listdir(PerspectiveFolder):
        imageToRemove = PerspectiveFolder + "\\" + imagefile 
        os.remove(imageToRemove)

    Napravi_Ga_Savku()
    Resolution = scene_resolution()
    frameRange = scene_frameRange()
    print ("Resolution: {}".format(Resolution))
    print ("frameRange: {}".format(frameRange))
   # mc.playblast(widthHeight=(0,0),format="image",filename=PerspectiveName,percent=100,showOrnaments=False,viewer=False,forceOverwrite=True)
    mc.playblast(widthHeight=Resolution,format="image",filename=PerspectiveName,percent=100,showOrnaments=False,viewer=False,forceOverwrite=True)

    # Restore Default Colors
    mc.displayRGBColor('background',Original_BG_R,Original_BG_G,Original_BG_B)
    mc.displayRGBColor('backgroundTop',Original_BGT_R,Original_BGT_G,Original_BGT_B)
    mc.displayRGBColor('backgroundBottom',Original_BGB_R,Original_BGB_G,Original_BGB_B)


    CleanUp2()

