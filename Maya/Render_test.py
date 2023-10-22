#######################################################
###    Matchmove RenderSetup                        ###
###                                                 ###
###    Just follow the instructions on the windows  ###
###                                                 ###
###    Created by                                   ###
###    Aleksandar Trajkovski                        ###
###    Damjan Ristov                                ###
###    - Remade the script                          ###  
###                                                 ###
###    v2.0                                         ###
###                                                 ###
####################################################### 
    



from doctest import master
import sys
import itertools
import os
import maya.mel as mel
import string


import maya.app.renderSetup.model.override as override
import maya.app.renderSetup.model.selector as selector
import maya.app.renderSetup.model.collection as collection
import maya.app.renderSetup.views.overrideUtils as utils
import maya.app.renderSetup.model.renderLayer as renderLayer
import maya.app.renderSetup.model.renderSetup as renderSetup
import maya.cmds as mc
import time
from collections import OrderedDict
from functools import partial

#### Tons of global, maybe should try to simplify them


global lidar
global persp
global items
global CleanNameItems
global BkcItems
global Bkc
global Fln
global rigGeo
global RBkc
global RFln
global RigList
global LidarList
global corresponding
global DisplayNameLayer
global RenderNameLayer
global GeoCollection
global RigCounter
global LidarCounter
global OriginalGreen
DisplayNameLayer = []
RenderNameLayer = []
corresponding = []
RigList = []
LidarList = []
BkcItems = []
items=[]
CleanNameItems = []


RigCounter = 0
LidarCounter = 0
OriginalGreen = 1.0


Bkc = 0
Fln = 0


RFln = 0
RBkc = 0


lidar = 0
persp = 0


def CleanUp():
    mc.modelEditor('modelPanel4' , edit = True, lw=1.0,interactive=True)
    rs = renderSetup.instance()
    rs.clearAll()
    master= rs.getDefaultRenderLayer()
    master.setRenderable(False)
    layers= mc.ls(long=True,type="displayLayer")
    for layer in layers:
        if "defaultLayer" not in layer:
            mc.delete(layer)


FullMayaPath = mc.file(q=True,sn=True)
ActualMayaPath = FullMayaPath.split("/")
MayaFolder = FullMayaPath.split("/")
del MayaFolder[-1]


for MayaFolda in MayaFolder[::-1]:
 
    if MayaFolda != "main3d" :
        MayaFolder.remove(MayaFolda)
    elif MayaFolda == "main3d":
        break
MayaFolder = "/".join(MayaFolder)
MayaName = mc.file(q=True,sn=True,shn=True)
ActualName = MayaName.split("_")
ActualName = list(OrderedDict.fromkeys(ActualName))
for i in ActualName[::-1]:
    ActualName.remove(i)
    if i == "main3d" or i=="trackScene":
        break
for j in ActualMayaPath[::-1]:
    ActualMayaPath.remove(j)
    if j == "main3d":
        break
for n, k in enumerate(ActualMayaPath):
    if k == "3d_comp":
        ActualMayaPath[n] = "render"


def FindMayaVersion():
    MayaActual,ext = os.path.splitext(MayaName)
    SplitMayaName = MayaActual.split("_")
    print ("SplitMayaName = {}".format(SplitMayaName))
    for q in reversed(SplitMayaName):
        if "v00" in q:
            return (q)


Version = FindMayaVersion()
print ("Version = {}".format(Version))
VersionPath = "/".join(ActualMayaPath) + "/main3d/" + Version + "/"
print("VersionPath = {}".format(VersionPath))
if not os.path.exists(VersionPath):
    original_umask = os.umask(0)
    os.makedirs(VersionPath,mode=0o777  )
MayaRenderPath = "/".join(ActualMayaPath) + "/main3d/" + Version + "/"
ShotName = "_".join(ActualName)



print("FullMayaPath = {}".format(FullMayaPath))
print("ActualMayaPath = {}".format(ActualMayaPath))
print("MayaFolder = {}".format(MayaFolder))
print("MayaRenderPath = {}".format(MayaRenderPath))
print("MayaName = {}".format(MayaName))
print("ActualName = {}".format(ActualName))
print("ShotName = {}".format(ShotName))


mc.workspace(fr=["images", MayaRenderPath])
mc.workspace(u=True)
List_WS = mc.workspace(l=True)
print("List_WS = {}".format(List_WS))
mc.workspace(s=True)
mc.setMenuMode("renderingMenuSet")


ProjectName = MayaRenderPath.split("/")[:-5]
ProjectName = ProjectName[-1]
StudioName = MayaRenderPath.split("/")[:-6]
StudioName = StudioName[-1]
print("ProjectName: {}".format(ProjectName))
print("StudioName: {}".format(StudioName))
       


def RSWindow():
    
    """Choosing which camera you need to use to render (usually undist) and some addition option"""
    
    global lidar
    global RSwindow
    lidar = 0
    mc.setAttr('defaultRenderGlobals.currentRenderer', 'mayaHardware2', type='string')
    mc.setAttr ("hardwareRenderingGlobals.lineAAEnable", 0)
    mc.setAttr ("hardwareRenderingGlobals.lineAAEnable", 1)
    mc.setAttr ("hardwareRenderingGlobals.multiSampleEnable", 0)
    mc.setAttr ("hardwareRenderingGlobals.multiSampleEnable", 1)
    mc.setAttr ("hardwareRenderingGlobals.ssaoEnable", 0)
    mc.setAttr ("hardwareRenderingGlobals.lightingMode", 0)
    mc.setAttr ("hardwareRenderingGlobals.renderMode", 5)
    
    RSwindow = mc.window( title="Render Settings", iconName='RS', w=(600), h=100 )
    mc.columnLayout( adjustableColumn=True )
    mc.text(label='Select the camera you will render from then\n select Next and choose which resolution you need\n and do you need to render perspective',w=200, h=100,rs=1)
    mc.rowLayout(nc=2)
    mc.button(w=300, h=50, label='Next', command=('RendSett()') )
    mc.button(w=300, h=50, label='Exit', command=('cmds.deleteUI(\"' + RSwindow + '\", window=True)') )
    mc.setParent( '..' )
    mc.showWindow( RSwindow )


#    global ConesGeoRigMenu                        
#    ConesGeoRigMenu   = mc.window( title="Camera", iconName='Camera', w=(800), h=100 )
#    mc.columnLayout( adjustableColumn=True )
#    mc.text(label='Select camera to pack Camera, Select geo\lidar to pack geo,Select rig to pack rig, \n Delete everything else ',w=200, h=100,rs=1)
#    mc.rowLayout(nc=4)
#    mc.button(w=200, h=50, label='Camera', command=('TippetCamera()'))
#    mc.button(w=200, h=50, label='Geo', command=('TippetGeo()'))
#    mc.button(w=200, h=50, label='Rig', command=('TippetRig()'))
#    mc.button(w=200, h=50, label='Exit', command=('cmds.deleteUI(\"' + ConesGeoRigMenu  + '\", window=True)') )
#    mc.setParent( '..' )
#    mc.showWindow(ConesGeoRigMenu) 
    
def RendSett():
    
    global RSwindow
    global persp
    persp = 0
    startF = int(cmds.playbackOptions(min=True, q=True))
    endF = int(cmds.playbackOptions(max=True, q=True))
    
    CleanCam = mc.ls(type='camera')
       
    CleanCam_shape = mc.listRelatives(CleanCam, c=1)
        
    for i in range(len(CleanCam)):
       mc.setAttr( CleanCam[i] + ".renderable",0)
        
    
    #### chose the camera you need
    
    cam = mc.ls(sl=1)[0]
    cam_shape = mc.listRelatives(cam, c=1)
    cam_image = mc.listRelatives(mc.listConnections(cam_shape[0]), c=True)

    ### Tippett: Getting Focal Length:
    if StudioName == "Tippett":
    #    FL = mc.getAttr(cam_shape[0] + ".focalLength")
    #    FL = round(FL,2)
        ###

        try:
            cam = mc.ls(sl=True)[0]
            cam_shape = mc.listRelatives(cam, c=True)
            fl = mc.listConnections(cam_shape)[0]
            if mc.objectType(fl) != "animCurveTU":
                fl = mc.listConnections(cam_shape)[1]
                if mc.objectType(fl) != "animCurveTU":
                    fl = mc.listConnections(cam_shape)[2]
                
            flList = mc.keyframe(fl, q=True, absolute=True, valueChange=True);
            
            flMax = max(flList)
            flMin = min(flList)
            FL = str("%.2f" %flMin) + '-' + str("%.2f" %flMax)
        except:
            cam = mc.ls(sl=True)[0]
            cam_shape = mc.listRelatives(cam, c=True)
            FL = str("%.2f" %mc.getAttr(cam_shape[0] + ".focalLength"))

                

        ###
        print("FL={}".format(FL))

        with open ("{}/Focal Length.txt".format(MayaFolder),"w") as file:
            Focal = "FocalLength={}".format(FL)
            file.writelines(Focal)

    MaxW = float((mc.getAttr(cam, cam_image[0] + ".coverageX")))    
    MaxH = float((mc.getAttr(cam, cam_image[0] + ".coverageY")))
    print ("MaxW: {}".format(MaxW))  
    print ("MaxH: {}".format(MaxH))


    Division = (MaxW/MaxH)
    print ("Division: {}".format(Division))  
        
    mc.setAttr(cam_shape[0] + ".farClipPlane", 10000000)
    mc.setAttr(cam_shape[0] + ".nearClipPlane", 1)
    mc.setAttr("perspShape.renderable", 0)
    mc.setAttr("topShape.renderable", 0)
    mc.setAttr("frontShape.renderable", 0)
    mc.setAttr("sideShape.renderable", 0)
    mc.setAttr( cam_shape[0] + ".renderable",1)
    mc.renderSettings(cam = "cam_shape" )
    mc.setAttr("defaultRenderGlobals.imageFormat",3)
    mc.setAttr("defaultRenderGlobals.tiffCompression",1)
    mc.setAttr("defaultRenderGlobals.outFormatControl",0)
    mc.setAttr("defaultRenderGlobals.animation",1)
    mc.setAttr("defaultRenderGlobals.putFrameBeforeExt",1)
    mc.setAttr("defaultRenderGlobals.extensionPadding",4)
    mc.setAttr("defaultRenderGlobals.startFrame", startF)
    mc.setAttr("defaultRenderGlobals.endFrame", endF)
    mc.setAttr("defaultResolution.w", MaxW)
    mc.setAttr("defaultResolution.h", MaxH)
    mc.setAttr("defaultResolution.pixelAspect",1.0)
    mc.setAttr("defaultResolution.deviceAspectRatio",(MaxW/MaxH))
    DevAspRatio = mc.getAttr("defaultResolution.deviceAspectRatio")
    if Version:
        mc.setAttr("defaultRenderGlobals.imageFilePrefix","<RenderLayer>/<RenderLayer>" + "_" + Version, type='string')
    else:
        mc.setAttr("defaultRenderGlobals.imageFilePrefix","<RenderLayer>/<RenderLayer>", type='string')
    print ("DevAspRatio: {}".format(DevAspRatio))


    ConesGeoRigMenu()
    mc.deleteUI( RSwindow, window=True )
    AssignRenderGeo()
    
       


def AssignRenderGeo():
    
    AllGeo= mc.listRelatives(mc.ls(type='mesh'), p = True, f = True)
    
##### Create material for render


    myLambert = mc.shadingNode( 'lambert', asShader=True )
    mc.select(AllGeo)
    mc.hyperShade( assign=myLambert ) 
    mc.setAttr (myLambert+".color" ,0, 0, 0, type='double3')
    mc.setAttr (myLambert+".diffuse", 0)
    mc.setAttr ("lambert1.color" , 0, 0, 0, type='double3')
    mc.setAttr ("lambert1.diffuse", 0)

    mc.modelEditor('modelPanel4' , edit = True, lw=2.0,interactive=True)
    
def ConesGeoRigMenu():
    global ConesGeoRigMenu
    global ConesButton
    global GeoButton
    global LidarButton
    global RigButton    

    startF = int(cmds.playbackOptions(min=True, q=True))
    endF = int(cmds.playbackOptions(max=True, q=True))

    ConesGeoRigMenu   = mc.window( title="RenderSetup", iconName='Camera', w=(800), h=100 )
    mc.columnLayout( adjustableColumn=True )
    mc.text(label='Select Cones, Geo , and Rigs(if any)',w=200, h=100,rs=1)
    mc.rowLayout(nc=7)
    ConesButton = mc.button(w=200, h=50, label='Cones / Horizon', command=('Cones()'),backgroundColor=(1.0,0.0,1.0))
    try:
        if StudioName == "ImageEngine":
            LidarButton = mc.button(w=200, h=50, label='Lidar', command=('SelectLidar()'),backgroundColor=(0.57,0.14,-0.42))
        else:
            GeoButton = mc.button(w=200, h=50, label='Geo', command=('SelectGeo()'),backgroundColor=(1.0,1.0,0.0))
    except:
        GeoButton = mc.button(w=200, h=50, label='Geo', command=('SelectGeo()'),backgroundColor=(1.0,1.0,0.0))
    RigButton = mc.button(w=200, h=50, label='Rig', command=('SelectRig()'),backgroundColor=(0.0,1.0,1.0))
    FinishButton = mc.button(w=200, h=50, label='Finish', command=('Finish()') ,backgroundColor=(1.0,0.2,0.3))
    mc.setParent( '..' )

    
    def get_Slider_Value(slider):
        value = cmds.intSliderGrp(slider,q=True,value=True)
        return value

    def set_StartFrame(slider,*args,**kwargs):
        value = get_Slider_Value(slider)
        mc.setAttr("defaultRenderGlobals.startFrame", value)
    def set_EndFrame(slider,*args,**kwargs):
        value = get_Slider_Value(slider)
        mc.setAttr("defaultRenderGlobals.endFrame", value)
    def set_LineWidth(slider,*args,**kwargs):
        value = get_Slider_Value(slider)
        cmds.modelEditor('modelPanel4' , edit = True, lw=value,interactive=True)


    LW_Slider = cmds.intSliderGrp(label="LineWidth",min=1,max=5,value=2,step=1,dc='empty',columnWidth=(1,100),height=50,columnAlign=(1,"center"),field=True)
    Start_Frame_Slider = cmds.intSliderGrp(label="Start Frame",min=startF,max=endF,value=startF,step=1,dc='empty',columnWidth=(1,100),height=35,
                                            columnAlign=(1,"center"),field=True,backgroundColor=(0.33725,0.37647,0.46667),ebg=False)#86,96,119
    End_Frame_Slider = cmds.intSliderGrp  (label="End Frame",min=startF,max=endF,value=endF,    step=1,dc='empty',columnWidth=(1,100),height=35,
                                            columnAlign=(1,"center"),field=True,backgroundColor=(0.33725,0.46667,0.33725),ebg=False)#86,119,86

    cmds.intSliderGrp(LW_Slider,e=True,dc=partial(set_LineWidth,LW_Slider,x=1))
    cmds.intSliderGrp(Start_Frame_Slider,e=True,dc=partial(set_StartFrame,Start_Frame_Slider,x=1))
    cmds.intSliderGrp(End_Frame_Slider,e=True,dc=partial(set_EndFrame,End_Frame_Slider,x=1))
    mc.showWindow(ConesGeoRigMenu) 



def Cones():
    global ConesGeoRigMenu
    global ConesButton
    global Cwindow
    global DisplayNameLayer
    global RenderNameLayer
    rs = renderSetup.instance()
    
    cones=mc.ls( dag=True, g=1, ap=True, sl=True )    
    conesOrig = mc.listRelatives(mc.ls(cones), p = True)
           
    ConesName = "Cones_"
        
    mc.select(cones)
    AddCones = mc.createDisplayLayer (name= ConesName ,nr=1)
    mc.setAttr (ConesName  + ".displayType", 0) 
    mc.setAttr (ConesName  + ".color", 16)     
    mc.setAttr (ConesName  + ".overrideColorRGB", 0, 0, 0) 
    mc.setAttr (ConesName  + ".overrideRGBColors", 0)
    
    rl = rs.createRenderLayer("CONES")
    c1 = rl.createCollection(ConesName + "Mesh" )
    c1.getSelector().staticSelection.add(conesOrig)

    rs.switchToLayer(rl)
    visibleLayer = rs.getVisibleRenderLayer()

    col = visibleLayer.renderSettingsCollectionInstance()

    ov = col.createAbsoluteOverride('hardwareRenderingGlobals','renderMode')
    ov.setAttrValue(0)

    def createAbsoluteOverride():
        layer_name = 'CONES'  # any layer name
        collection_name = 'Cones_Mesh'  # any collection name
        target_collection = rs.getRenderLayer(layer_name).getCollectionByName(collection_name)
        mc.polyCube(n='dummyObj')
        abs_override = target_collection.createAbsoluteOverride('dummyObjShape', 'bck')
        abs_override.setName(layer_name + '_backfaceCulling')
        abs_override.setAttrValue(3)
        mc.delete('dummyObj')
        Emptycollection = rs.getRenderLayer(layer_name).getCollectionByName("_untitled_")
        print (Emptycollection)
        collection.delete(Emptycollection)

    createAbsoluteOverride()

#    for cone in cones:
#        mc.setAttr((cone + ".backfaceCulling"),3)
    #backfaceCullOverride = col.createAbsoluteOverride("pConeShape1","bck")
    #backfaceCullOverride.setAttrValue(3)

    rs.switchToLayer(master)
    # ConesWireOverride = rl.createAbsoluteOverride(AddCones, 'hardwareRenderingGlobals.renderMode')
    # ConesWireOverride.setAttrValue("Wire") 
    
    mc.button(ConesButton,edit=True, enable=False,backgroundColor=(0.335481,-0.664519,0.329037))
#    mc.button(GeoButton,edit=True, enable=False,backgroundColor=(0.333333,0.333333,-0.666667))
#    mc.button(RigButton,edit=True, enable=False,backgroundColor=(0.0,0.198892,1.0))
#   
#    GeoWindow()    
#    mc.deleteUI( Cwindow, window=True )
    



def GeoWindow():
    
    global Gwindow
    
    
    Gwindow = mc.window( title="Choose Geo", iconName='Geo', widthHeight=(600, 150) )
    mc.columnLayout( adjustableColumn=True )
    mc.text(label='Select Geo\Lidar then Press Next',w=100, h=100,rs=1)
    mc.rowLayout(nc=3)
    mc.button(label='Next',align='left',w=200, h=50, command=('SelectGeo()') )
    mc.button(w=200, h=50, label='Skip', command=("GeoSkipCmd()") )
    mc.button(label='EXIT',align='right',w=200, h=50,command=('cmds.deleteUI(\"' + Gwindow + '\", window=True)') )
    mc.setParent( '..' )
    mc.showWindow( Gwindow ) 


def GeoSkipCmd():
    RigWindow()
    mc.deleteUI( Gwindow, window=True )


def SelectGeo():
    
    global Gwindow
    global items
    global CleanNameItems
    global CleanGeoOrig
    global GeoCollection
    rs = renderSetup.instance()
        
    geo=mc.ls( dag=True, g=1, typ="mesh", ap=True, sl=True )
    GeoOrig = mc.listRelatives(mc.ls(geo),p=1)
    items.append(GeoOrig)
    GeoName = "Geo_"


    mc.select(geo)
    AddGeo = mc.createDisplayLayer (name= GeoName ,nr=1)
    DisplayNameLayer.append(AddGeo)
    mc.setAttr (GeoName  + ".displayType", 0) 
    mc.setAttr (GeoName  + ".color", 16)     
    mc.setAttr (GeoName  + ".overrideColorRGB", 0, 0, 0) 
    mc.setAttr (GeoName  + ".overrideRGBColors", 0)
    
    rl = rs.createRenderLayer("GEO")
    RenderNameLayer.append(rl)
    try:
        GeoCollection = rl.createCollection(GeoName + "Mesh" )
        GeoCollection.getSelector().staticSelection.add(GeoOrig)
    except:
        pass
    mc.button(GeoButton,edit=True, enable=False,backgroundColor=(0.333333,0.333333,-0.666667))                
#    RigWindow()
#    mc.deleteUI( Gwindow, window=True )

def SelectLidar():
    global LidarCounter
    global Gwindow
    global items
    global CleanNameItems
    global CleanGeoOrig
    global GeoCollection
    global LidarList
    rs = renderSetup.instance()
    LidarCounter += 1
        
    Lidar=mc.ls( dag=True, g=1, typ="mesh", ap=True, sl=True )
    LidarOrig = mc.listRelatives(mc.ls(Lidar),p=1)
    items.append(LidarOrig)
    LidarName = "Lidar_"

    LidarList.append(LidarOrig)

#    mc.select(Lidar)
#    AddLidar = mc.createDisplayLayer (name= LidarName ,nr=1)
#    DisplayNameLayer.append(AddLidar)
#    mc.setAttr (LidarName  + ".displayType", 0) 
#    mc.setAttr (LidarName  + ".color", 16)     
#    mc.setAttr (LidarName  + ".overrideColorRGB", 0, 0, 0) 
#    mc.setAttr (LidarName  + ".overrideRGBColors", 0)
    
#    rl = rs.createRenderLayer("LIDAR")
#    RenderNameLayer.append(rl)
#    try:
#        LidarCollection = rl.createCollection(LidarName + "Mesh" )
#        LidarCollection.getSelector().staticSelection.add(LidarOrig)
#    except:
#        pass
    if LidarCounter >= 3:
        mc.button(LidarButton,edit=True, enable=False,backgroundColor=(0.478005,0.043989,-0.521995))                
#    RigWindow()
#    mc.deleteUI( Gwindow, window=True )  
#               
def RigWindow():
    
    global Rwindow
    global BuckyCheckBox
    global FalconCheckBox
   
    Rwindow = mc.window( title="Choose Rig ", iconName='Rig', widthHeight=(600, 180) )
    mc.columnLayout( adjustableColumn=True )
    mc.text(label='Select Rig to add the list and press Finish when you are done adding',w=100, h=100,rs=1)
    BuckyCheckBox = mc.checkBox(align='left', label='Bucky Rig')
    FalconCheckBox = mc.checkBox(align='right', label='Falcon Rig')
    mc.rowLayout(nc=3)
    mc.button(label='Next',align='left',w=200, h=50, command=('SelectRig()') )
    mc.button(w=200, h=50, label='Finish', command=("Finish()") )
    mc.button(label='EXIT',align='right',w=200, h=50,command=('cmds.deleteUI(\"' + Rwindow + '\", window=True)') )
    mc.setParent( '..' )
    mc.showWindow( Rwindow )


def SelectRig():
    
    """ Working with newest bkc and fln rigs. Otherwise general for all other rigs\objects
    It will need updates as it goes with new rigs, new render passes and\or new projects"""
    
    global Bkc
    global Rwindow
    global items
    global CleanNameItems
    Bkc = 0
    global BArigGeo
    global FLNrigGeo
    global BAwindow
    global FalconCheckBox
    global FJPwindow
    global CleanRigGeoName
    global RigList
    global RigCounter
    global OriginalGreen
    Fln = 0
    RigCounter += 1
    Delighter = 0.20
    OriginalGreen = OriginalGreen - Delighter
    print ("RigCounter: {}".format(RigCounter))


    rigGeo = mc.ls( dag=True, typ="mesh", sl=True,ap=True,long=True )
    
    rigGeoOrig = mc.listRelatives(mc.ls(rigGeo), p = True, fullPath=True)
    
    items.append(rigGeoOrig)
#    CleanRigGeoOrig = rigGeoOrig[0].encode('ascii','ignore')        
#    CleanRigGeoName = CleanRigGeoOrig.split(':')        
#    CleanNameItems.append(CleanRigGeoName[0])
    RigList.append(rigGeoOrig) 
    print ("RigList: {}".format(RigList))


    for i in range(RigCounter):
        mc.button(RigButton,edit=True,backgroundColor=(0.0,OriginalGreen,1.0)) 
        
#        mc.confirmDialog(title='Confirm Window', message='Rig added to the list', button = ("OK"))
    
      
def Finish():
    
    """ Final step, need clean up, but it is working so we will see.Edge width and toon still a bit buggy
    mostly depends on the GPU and\or maya versions. Maya 2020 creates additional toons for no reason .Maybe refresh viewport"""
    
    rs = renderSetup.instance()
    
    global Rwindow
    global RBkc
    global RFln
    global GeoCollection


    DisAssembleList = []
    for sublist in items:
        for val in sublist:
            DisAssembleList.append(val)
        
    print ("DisAssembleList: {}".format(DisAssembleList)) 


#    DisplayNameLayer = []
#    RenderNameLayer = []
    print ("RenderNameLayer: {}".format(RenderNameLayer)) 
    print ("DisplayNameLayer: {}".format(DisplayNameLayer))
        
    
    Rig_index = 0
    Rig_Number = 0
    Lidar_index = 0
    Lidar_Number = 0
    


    print ("Items: {}".format(items))         
    print ("CleanNameItems: {}".format(CleanNameItems))       
#    print ("rigGeoOrig: {}".format(rigGeoOrig))    
    print ("RigList: {}".format(RigList))
    
    for (RigName) in (RigList):
        print ("RigName: {}".format(RigName)) 
        mc.select(RigName)
        if (Rig_index) == 0:
            Created = mc.createDisplayLayer (name = "RIG"+"_",nr=1)
        else:
            Created = mc.createDisplayLayer (name = "RIG"+"_"+str(Rig_Number),nr=1)     
        DisplayNameLayer.append(Created)
        mc.setAttr (Created  + ".displayType", 0) 
        mc.setAttr (Created  + ".color", 16)     
        mc.setAttr (Created + ".overrideColorRGB", 0, 0, 0) 
        mc.setAttr (Created+ ".overrideRGBColors", 0)
        
        if (Rig_index) == 0:
            rlRender = rs.createRenderLayer("RIG")
        else:
            rlRender = rs.createRenderLayer("RIG"+str(Rig_Number))   
        RenderNameLayer.append(rlRender)        
        c1Render = rlRender.createCollection(RigName[0] + "Mesh" )
        Rig_Number+=1
        Rig_index +=1 
        for item in items:
            c1Render.getSelector().staticSelection.add(item) 
        try:
            for item in items:
                GeoCollection.getSelector().staticSelection.add(item)
        except:
            pass
    print ("RenderNameLayer: {}".format(RenderNameLayer)) 
    print ("DisplayNameLayer: {}".format(DisplayNameLayer)) 
    
    if StudioName == "ImageEngine":
        for (LidarName) in (LidarList):
            print ("LidarName: {}".format(LidarName)) 
            mc.select(LidarName)
            if (Lidar_index) == 0:
                Created = mc.createDisplayLayer (name = "LIDAR"+"_",nr=1)
            else:
                Created = mc.createDisplayLayer (name = "LIDAR"+"_"+str(Lidar_Number),nr=1)     
            DisplayNameLayer.append(Created)
            mc.setAttr (Created  + ".displayType", 0) 
            mc.setAttr (Created  + ".color", 16)     
            mc.setAttr (Created + ".overrideColorRGB", 0, 0, 0) 
            mc.setAttr (Created+ ".overrideRGBColors", 0)
            
            if (Lidar_index) == 0:
                rlRender = rs.createRenderLayer("LIDAR")
            else:
                rlRender = rs.createRenderLayer("LIDAR"+str(Lidar_Number))   
            RenderNameLayer.append(rlRender)        
            c1Render = rlRender.createCollection(LidarName[0] + "Mesh" )
            Lidar_Number+=1
            Lidar_index +=1 
            for item in items:
                c1Render.getSelector().staticSelection.add(item) 
            try:
                for item in items:
                    GeoCollection.getSelector().staticSelection.add(item)
            except:
                pass 
        
    for i in range(len(DisplayNameLayer)):
    
        for n in range(len(RenderNameLayer)):
            
            if i !=n:                            
                OvGeo = RenderNameLayer[i].createConnectionOverride(DisplayNameLayer[n], 'displayType')
                OvGeo.setAttrValue(2.0)    
            
    if lidar == 1:
        
        OvLidar = RenderNameLayer[0].createConnectionOverride('hardwareRenderingGlobals','multiSampleEnable')
        OvLidar.setAttrValue(0.0) 
    
    if RBkc == 1:
        
           RDbkc = DisplayNameLayer.index ('buckyR22LDisplayRender')
           
           bkToonLayer =  RenderNameLayer[RDbkc].createCollection('BkcToonLayer')
           mc.select('BkcToonShader')
           bkToonLayer.getSelector().staticSelection.add(mc.ls(sl=1))
           mc.select(d=1)
           bkToonOv = RenderNameLayer[RDbkc].createConnectionOverride(DisplayNameLayer[RDbkc], 'visibility')
           bkToonOv.setAttrValue(0.0)
           
    if RFln == 1:


        RDfln = DisplayNameLayer.index ('falconR5LDisplayRender')        
        FlnToonLayer =  RenderNameLayer[RDfln].createCollection('FlnToonLayer')
        mc.select('FlnToonShader')
        FlnToonLayer.getSelector().staticSelection.add(mc.ls(sl=1))
        mc.select(d=1)
        FlnToonOv = RenderNameLayer[RDfln].createConnectionOverride(DisplayNameLayer[RDfln], 'visibility')
        FlnToonOv.setAttrValue(0.0)


              
    mc.select(d=1)
    mc.deleteUI( ConesGeoRigMenu, window=True )
    #mc.modelEditor('modelPanel4' , edit = True, lw=2.0,interactive=True)
    mc.savePrefs( general=True)
    SetPixelAspect()
  
def ResetEdgeWidth():
    
    mc.modelEditor('modelPanel4' , edit = True, lw=1)


def SetPixelAspect():
    Pixel = mc.getAttr("defaultResolution.pixelAspect")
    print ("BeforePixel: {}".format(Pixel)) 
    mc.setAttr("defaultResolution.pixelAspect",1.0)
    Pixel = mc.getAttr("defaultResolution.pixelAspect")
    print ("AfterPixel: {}".format(Pixel)) 
    try:
        exec(open('//fs3/Sh1/uber/Master/MayaScripts_2018/main_scripts/PixelAspect.py'), locals(), globals()) 
    except:
        pass


RSWindow() 
CleanUp()



                