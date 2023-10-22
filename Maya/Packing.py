import sys
import itertools
import os
import maya.mel as mel
import string
import maya.cmds as mc

tool = "mmSceneSetup"
version = "001"

def ChooseStudio():
    
#    TypeRender=mc.confirmDialog(title='Studio',icon='question', message='Choose Studio packing', button=['ImageEngine','CraftyApes','Tippet','ChickenBone'])
#    if TypeRender =='ImageEngine':
#        CreateFolders()
#    elif TypeRender == 'CraftyApes':
#        CraftyStart()
#    elif TypeRender == 'Tippet':
#        TippetPackingWindow() 
#    elif TypeRender == 'ChickenBone':
#        ChickenBoneStart()
#    ImageEngineButton = mc.button(w=100, h=50, label='ImageEngine', command=('CreateFolders()'),backgroundColor=(-0.053333,4.166666,0.386667))
#    CrafyApesButton = mc.button(w=100, h=50, label='CrafyApes', command=('CraftyStart()'),backgroundColor=(0.59,0.44,0.954651))
#    TippettButton = mc.button(w=100, h=50, label='Tippett', command=('TippetPackingWindow()'),backgroundColor=(0.095,0.008,2.04))
#    FinishButton = mc.button(w=100, h=50, label='ChickenBone', command=('ChickenBoneStart()') ,backgroundColor=(1.076666,0.256668,0.166666))

    global ChooseStudioMenu
               
    ChooseStudioMenu   = mc.window( title="Choose Studio", iconName='Camera', w=(500), h=100 )
    mc.columnLayout( adjustableColumn=True )
    mc.text(label='Choose which studio you wish to pack for',w=200, h=100,rs=1)
    mc.rowLayout(nc=5)
    ImageEngineButton = mc.button(w=100, h=50, label='ImageEngine', command=('CreateFolders()'))
    CrafyApesButton = mc.button(w=100, h=50, label='CrafyApes', command=('CraftyStart()'))
    TippettButton = mc.button(w=100, h=50, label='Tippett', command=('TippetPackingWindow()'))
    FramestoreButton = mc.button(w=100, h=50, label='Framestore', command=('Framestore_Menu()'))
    FinishButton = mc.button(w=100, h=50, label='ChickenBone', command=('ChickenBoneStart()'))
    mc.setParent( '..' )
    mc.showWindow(ChooseStudioMenu)  

def WhichCamera():
    
    global WCwindow
    
    """Choosing camera and points group you need """
    
    WCwindow = mc.window( title="Camera", iconName='RS', w=(600), h=100 )
    mc.columnLayout( adjustableColumn=True )
    mc.text(label='Select the camera and point group',w=200, h=100,rs=1)
    mc.rowLayout(nc=2)
    mc.button(w=300, h=50, label='Next', command=('ApplyCamera()') )
    mc.button(w=300, h=50, label='Exit', command=('mc.deleteUI(\"' + WCwindow + '\", window=True)') )
    mc.setParent( '..' )
    mc.showWindow( WCwindow )
    
def ApplyCamera(): 

    global WCwindow
    
    CamNCp = mc.ls(sl=1)
    mc.parent(CamNCp,"mmScene_camera_GRP")
    
    ConesHorizon()
    
    mc.deleteUI( WCwindow, window=True )
    
   
def ConesHorizon():
    
    global CHwindow
    
    """Choosing cones and horizon you need """
    
    CHwindow = mc.window( title="Cones", iconName='Cones', w=(600), h=100 )
    mc.columnLayout( adjustableColumn=True )
    mc.text(label='Select trackers for cones ',w=200, h=100,rs=1)
    mc.rowLayout(nc=2)
    mc.button(w=300, h=50, label='Next', command=('ApplyCones()') )
    mc.button(w=300, h=50, label='Exit', command=('mc.deleteUI(\"' + CHwindow + '\", window=True)') )
    mc.setParent( '..' )
    mc.showWindow( CHwindow )
    
def ApplyCones(): 
    
    global CHwindow
    locators = mc.ls(sl=True)
    for i in range(len(locators)):
        cone1=mc.polyCone(r=1, h=2, sx=8, sy=1, sz=0, ax=(0, 1, 0), rcp=0, cuv=3, ch=1)[0]
        mc.move(0, -1, 0, r=True, os=True, wd=True)
        mc.xform(sp=(0, 1, 0), rp=(0, 1, 0))
        mc.rotate(180, 0, 0, r=True, os=True, fo=True)
        mc.scale(0.5, 0.75, 0.5)
        mc.makeIdentity(apply=True, t=1, r=1, s=1, n=0, pn=1)
        mc.scale(2,2,2)
        locator_pos = mc.xform(locators[i], t=True, q=True, ws=True)
        mc.xform(cone1, t=locator_pos)
  
        mc.parent(cone1,"cone_GRP")
    mc.polyTorus(n = 'horizon', sr=20, sa= 200, sh= 200, r= 100000)     
    mc.parent("horizon","sphere_GRP")
    AssetsImage()
    mc.deleteUI( CHwindow, window=True )
    
    

def AssetsImage():
    
    
    global AIwindow
    """Choosing image engine assets you need """
    
    AIwindow = mc.window( title="Assets", iconName='Assets', w=(600), h=100 )
    mc.columnLayout( adjustableColumn=True )
    mc.text(label='Select image engine assets',w=200, h=100,rs=1)
    mc.rowLayout(nc=2)
    mc.button(w=300, h=50, label='Next', command=('ApplyAssets()') )
    mc.button(w=300, h=50, label='Exit', command=('mc.deleteUI(\"' + AIwindow + '\", window=True)') )
    mc.setParent( '..' )
    mc.showWindow( AIwindow )
    
def ApplyAssets(): 
    
    global AIwindow
    IMA = mc.ls(sl=1)
    mc.parent(IMA,"mmScene_asset_GRP")
    AssetsVertigo()
    mc.deleteUI( AIwindow, window=True )
    mel.eval("namespaceEditor")
    
    
    
def AssetsVertigo():
    
    global Verwindow
    
    """Choosing vertigo assets you need """
    
    Verwindow = mc.window( title="Vertigo Assets", iconName='VertigoAssets', w=(600), h=100 )
    mc.columnLayout( adjustableColumn=True )
    mc.text(label='Select vertigo assets',w=200, h=100,rs=1)
    mc.rowLayout(nc=2)
    mc.button(w=300, h=50, label='Next', command=('ApplyVertigoAssets()') )
    mc.button(w=300, h=50, label='Exit', command=('mc.deleteUI(\"' + Verwindow + '\", window=True)') )
    mc.setParent( '..' )
    mc.showWindow( Verwindow )

    
def ApplyVertigoAssets(): 
    
    global Verwindow
    IMA = mc.ls(sl=1)
    mc.parent(IMA,"wireBlue_GRP")
    mc.deleteUI( Verwindow, window=True )
    
#########################################################################################################################################################################################
#########################################################################################################################################################################################

def Framestore_Menu():
    global Framestore_Menu
    
    global CameraButton
    global RigsButton

    global ConesButton        
    global HorizonGeoButton            
    global LidarButton

    
    global FinishButton

    
    Framestore_Menu   = mc.window( title="Framestore Packing", iconName='Camera', w=(650), h=100 ,sizeable=False)
    mc.columnLayout( adjustableColumn=True )
    mc.text(label='''It's time to choose''',w=100, h=50,rs=1)
    mc.rowLayout(nc=6)

    ConesButton = mc.button(w=180, h=50, label='Cones', command=('F_Cones()'),backgroundColor=(0.26875,0.466768,1.0))
    HorizonGeoButton = mc.button(w=180, h=50, label='Horizon/Vertigo Geo', command=('F_HorizonGeo()'),backgroundColor=(0.669774,0.195175,1.0))
    LidarButton = mc.button(w=180, h=50, label='Lidar', command=('F_Lidar()'),backgroundColor=(0.668609,0.256707,0.0))
    RigsButton = mc.button(w=180, h=50, label='Rigs', command=('F_NameSpace()'),backgroundColor=(0.0,1.0,0.278497))
    CameraButton = mc.button(w=180, h=50, label='Camera', command=('F_Camera()'),backgroundColor=(0.545772,0.76982,1.0))
    
    

    mc.setParent( '..' )
    mc.rowColumnLayout(numberOfColumns=2)
    FinishButton = mc.button(w=908, h=50, label='Finish', command=('F_Finish()'),align='center' ,backgroundColor=(1.0,0.2,0.3))


    mc.showWindow(Framestore_Menu) 
    mc.deleteUI( ChooseStudioMenu, window=True )

#########################################################################################################################################################################################
#########################################################################################################################################################################################
def F_Cones():
    mc.button(ConesButton,edit=True, enable=False,backgroundColor=(0.025,0.016,0.035))
    Cones_Selection = cmds.ls(sl=True)
    if len(Cones_Selection) == 1:
        cones=cmds.polySeparate(Cones_Selection,n="trackingCone")
        
        parent = list(set(cmds.listRelatives(p=True)))
        print(parent)
        inkrement = "0000"
        Renamed_Cones = []
        for c in cones:
            inkrement = str(int(inkrement) + 1).zfill(len(inkrement))
            cmds.rename(c,"trackingCone{}_GEP".format(inkrement))
            Renamed_Cones.append(c)
    else:
        cones = Cones_Selection
        inkrement = "0000"
        Renamed_Cones = []
        for c in cones:
            inkrement = str(int(inkrement) + 1).zfill(len(inkrement))
            cmds.rename(c,"trackingCone{}_GEP".format(inkrement))
            Renamed_Cones.append(c)
            
    Renamed_Cones_Selection = cmds.ls(sl=True)  
    print("Renamed_Cones = {}".format(Renamed_Cones)) 
    print("Renamed_Cones_Selection = {}".format(Renamed_Cones_Selection))  
    ConesGroup = cmds.group(Renamed_Cones_Selection,name="trackingCones_GRP")
    ConesGroup_Selection = cmds.ls(ConesGroup,sl=True)
    
    if cmds.objExists("setGeo_GRP"):
        cmds.parent(ConesGroup_Selection,"setGeo_GRP")
    else:
        cmds.group(n="setGeo_GRP",world=True)


    cmds.delete(Renamed_Cones_Selection, constructionHistory=True)

    
#F_Cones()


def F_HorizonGeo():
    mc.button(HorizonGeoButton,edit=True, enable=False,backgroundColor=(0.157667,-0.089333,0.351667))
    HorizonGeoSelection = cmds.ls(sl=True)
    HGS_Parent_Status = cmds.listRelatives(HorizonGeoSelection,parent=True)
    if HGS_Parent_Status != None:
        HGS_Parent = list(set(HGS_Parent_Status))
    else:
        HGS_Parent = ["None"]
    print("HGS_Parent_Status = {}".format(HGS_Parent_Status))
    print("HGS_Parent = {}".format(HGS_Parent))  
        
    if cmds.objExists("trackingGeo_GRP"):
        if not "trackingGeo_GRP" in HGS_Parent:
            cmds.parent(HorizonGeoSelection,"trackingGeo_GRP")
        for HGS in HorizonGeoSelection:
            SplitHGS = HGS.split("_")
            LastSlog_HGS = SplitHGS[-1]
            if not LastSlog_HGS == "GEP":
                cmds.rename(HGS,HGS +"_GEP")
    else:
        for HGS in HorizonGeoSelection:
            SplitHGS = HGS.split("_")
            LastSlog_HGS = SplitHGS[-1]
            if not LastSlog_HGS == "GEP":
                cmds.rename(HGS,HGS +"_GEP")
        HorizonGeo_Group = cmds.group(n="trackingGeo_GRP")
        if cmds.objExists("setGeo_GRP"):
            cmds.parent(HorizonGeo_Group,"setGeo_GRP")
        else:
            cmds.group(n="setGeo_GRP",world=True)
#F_HorizonGeo()
def F_Lidar():
    mc.button(LidarButton,edit=True, enable=False,backgroundColor=(-0.159,0.057,0.282))
    LidarSelection = cmds.ls(sl=True)
    if cmds.objExists("model_GRP"):
        cmds.parent(LidarSelection,"model_GRP")
    else:
        Model_Group = cmds.group(n="model_GRP")
        if cmds.objExists("setLidar_GRP"):
            cmds.parent(Model_Group,"setLidar_GRP")
        else:
            cmds.group(n="setLidar_GRP",world=True)


def TypeNamespace():
    Namespace = cmds.promptDialog(
    title="Namespace",
    message= "Enter Namespace",
    button=['Ok',"Cancel"],
    defaultButton = "Ok",
    cancelButton = "Cancel",
    dismissString= "Cancel",
    )
    if Namespace == "Ok":
        text = cmds.promptDialog(query=True,text=True)
    return text

def F_NameSpace():
    mc.button(RigsButton,edit=True, enable=False,backgroundColor=(0.025,0.016,0.035))
    import pymel.core as pm

    RigSelection = pm.selected()
    Rig_Increment = "01"
    Rig_Secrement = "00"
    First_Slog_LIST = []
    Last_Slog_LIST = []
    for n in RigSelection:
        Namespace = n.namespace()
        print("Namespace = {}".format(Namespace))

        if Namespace != "":
            NameSpace_Divided = Namespace.split("_")
            First_Slog = Namespace.split("_")[0]
            First_Slog_LIST.append(First_Slog)

    l = First_Slog_LIST

    s = set(l)
    Duplicate_First_Slog_LIST=[]

    for x in l:
        if x in s:
            s.remove(x)
            print(s)
        else:
            Duplicate_First_Slog_LIST.append(x)

    print("Duplicate_First_Slog_LIST = {}".format(Duplicate_First_Slog_LIST)) 


    for n in RigSelection:
        Namespace = n.namespace()
        print("Namespace = {}".format(Namespace)) 
        if Namespace != "":
            NameSpace_Divided = Namespace.split("_")
            First_Slog = Namespace.split("_")[0]
            Last_Slog = Namespace.split("_")[-1]
            print("First_Slog = {}".format(First_Slog))
            last_first = First_Slog[-2]
            last_second = First_Slog[-1]
            print("last_first = {}".format(last_first)) 
            print("last_second = {}".format(last_second)) 

            if last_first.isdigit() and last_second.isdigit():
                print("both are digits")
                
            else:
                if First_Slog not in Duplicate_First_Slog_LIST:

                    First_Slog = First_Slog + "{}".format(Rig_Increment)
                    print("Altered_First_Slog = {}".format(First_Slog))
                    NameSpace_Divided[0] = First_Slog
                    NameSpace_Divided = "_".join(NameSpace_Divided) 
                    NameSpace_Divided = NameSpace_Divided.split(":")
                    NameSpace_Divided.pop()
                    NameSpace_Divided = "_".join(NameSpace_Divided)    
                    print("NameSpace_Divided = {}".format(NameSpace_Divided))
                else:
                    Rig_Secrement = str(int(Rig_Secrement) + 1).zfill(len(Rig_Secrement))
                    First_Slog = First_Slog + "{}".format(Rig_Secrement)
                    print("Duplicate_First_Slog = {}".format(First_Slog))
                    Last_Slog_LIST.append(Last_Slog)
                    NameSpace_Divided[0] = First_Slog
                    NameSpace_Divided[-1] = Last_Slog_LIST[0]
                    NameSpace_Divided = "_".join(NameSpace_Divided) 
                    NameSpace_Divided = NameSpace_Divided.split(":")
                    NameSpace_Divided.pop()
                    NameSpace_Divided = "_".join(NameSpace_Divided)  
                    print("Duplicate_NameSpace_Divided = {}".format(NameSpace_Divided))
                    

                Namespace = Namespace.split(":")
                Namespace.pop()
                Namespace = "_".join(Namespace)  
                try:
                    cmds.namespace(add=NameSpace_Divided)
                except:
                    pass
                try:
                    cmds.namespace(mv=(n.namespace(),NameSpace_Divided))        # If it already exists
                except RuntimeError:
                    cmds.namespace(force=True,mv=(n.namespace(),NameSpace_Divided))
                try:
                    cmds.namespace(rm=Namespace)
                except:
                    pass
        else:
            Namespace = TypeNamespace()
            print("No Namespace becomes:{}".format(Namespace))
            try:
                cmds.namespace(add=Namespace)
            except:
                pass
            cmds.rename(str(n), ":".join(['{}'.format(Namespace),'{}'.format(n)]))

def F_Camera():
    cam = cmds.ls(sl=1)[0]
    cam_shape = cmds.listRelatives(cam, c=1)[0]
    cam_ip = cmds.listRelatives(cmds.listConnections(cam_shape, c=True))[0]
    cropPlates_path = cmds.getAttr(cam_ip + ".imn")
    print ("cropPlates_path = {}".format(cropPlates_path))

    crop_split = cropPlates_path.split("_")
    print("crop_split = {}".format(crop_split))

    crop_split_last = crop_split[-1]

    if "crop" in crop_split_last:
        print("Crop")
    else:
        cmds.confirmDialog(message="Camera is probably not CROP, check backplate and make sure undist_crop is named with '_crop' at the end",ann="BLA",title="Dva pati Meri, ednash sestra i")
    CameraSelection = cmds.ls(sl=True)
    if len(CameraSelection) > 1:
        cmds.confirmDialog(message="More than 1 Camera object selected!",title="Brzi prsti")

    else:
        if cmds.objExists("Scene"):
            try:
                parent_Of_Camera=cmds.listRelatives(parent=True)
                if parent_Of_Camera[0] != "Scene":
                    cmds.parent(CameraSelection,"Scene")
            except:
                pass
        else:
            Scene_Group = cmds.group(n="Scene")
            cmds.parent(CameraSelection,"Scene")
            
        mc.button(CameraButton,edit=True, enable=False,backgroundColor=(0.025,0.016,0.035))
def F_Finish():
    mc.deleteUI( Framestore_Menu, window=True )
#########################################################################################################################################################################################
#########################################################################################################################################################################################
def IE_FoldersMenu():
    global IE_FoldersMenu
    
    global CameraButton
    global AssetsButton

    global ConesButton
    global SphereGridButton         #
    global RedHorizonButton            # RED
    global GreenGeoButton
    global BlueGeoButton
    global YellowGeoButton
    
    global FinishButton

    IE_FoldersMenu   = mc.window( title="IE Packing", iconName='Camera', w=(650), h=100 )
    mc.columnLayout( adjustableColumn=True )
    mc.text(label='''It's time to choose''',w=100, h=50,rs=1)
    mc.rowLayout(nc=9)

    CameraButton = mc.button(w=120, h=50, label='Camera', command=('CameraPack()'),backgroundColor=(0.14,0.54,1.0))
    AssetsButton = mc.button(w=120, h=50, label='Assets', command=('AssetsPack()'),backgroundColor=(0.0,0.57,0.30))
    ConesButton = mc.button(w=120, h=50, label='Cones', command=('ConesPack()'),backgroundColor=(1.0,0.11,0.87))
    RedHorizonButton = mc.button(w=120, h=50, label='Horizon', command=('HorizonPack()'),backgroundColor=(1.0,0.0,0.0))
    GreenGeoButton = mc.button(w=120, h=50, label='Green Geo', command=('GreenGeoPack()'),backgroundColor=(0.0,0.64,0.0))
    BlueGeoButton = mc.button(w=120, h=50, label='Blue Geo', command=('BlueGeoPack()'),backgroundColor=(0.019,0.120,0.64))
    
    YellowGeoButton = mc.button(w=120, h=50, label='Yellow Geo', command=('YellowGeoPack()'),backgroundColor=(1.0,1.0,0.0))
    SphereGridButton = mc.button(w=120, h=50, label='SphereGrid', command=('SphereGridPack()'),backgroundColor=(0.189,0.630,0.365))
    
    mc.setParent( '..' )
    mc.rowColumnLayout(numberOfColumns=2)
    FinishButton = mc.button(w=974, h=50, label='Finish', command=('Finish()'),align='center' ,backgroundColor=(1.0,0.2,0.3))


    mc.showWindow(IE_FoldersMenu) 

#########################################################################################################################################################################################
#########################################################################################################################################################################################
def Get_ShotName():
    FullMayaPath = mc.file(q=True,sn=True)
    ActualMayaPath = FullMayaPath.split("/")

    for j in ActualMayaPath[::-1]:
        ActualMayaPath.remove(j)
        if j == "main3d":
            break

    ShotName = ActualMayaPath[-1]
    print ("ShotName = {}".format(ShotName))
    SceneName = ShotName.split("_")[:-4]
    SceneNameJoined = "_".join(SceneName)
    print ("SceneName = {}".format(SceneName))
    print ("SceneNameJoined = {}".format(SceneNameJoined))
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
    
    
    return IE_ShotID,SceneNameJoined,ShotName

#########################################################################################################################################################################################
#########################################################################################################################################################################################
def CameraPack():
    IE_ShotID,SceneName,ShotName = Get_ShotName()            # Get ShotID and Scene Name
    #camera=mc.ls( dag=True, ap=True, sl=True )
    camera=mc.ls( sl=True )
     
          
    
    CameraGroupName = "Scene_" + SceneName + "_cam" + "_v01"
    print ("camera: {}".format(camera))
    mc.group(camera,name="Camera_Group")
    mc.parent("Camera_Group","mmScene_camera_GRP")
    # Rename the Camera
    mc.rename(camera,ShotName)
    # Rename the Group
    mc.rename("Camera_Group",CameraGroupName)
    mc.button(CameraButton,edit=True, enable=False,backgroundColor=(0.025,0.016,0.035))
def AssetsPack():
    assets=mc.ls(sl=True )
    assetsShape = mc.listRelatives(assets,ap=True,ad=True,fullPath=True) 
    print ("assets: {}".format(assets))
    print ("assetsShape: {}".format(assetsShape))     
    mc.select(assets)
    #mc.parent(assetsShape,"mmScene_asset_GRP",absolute=True)
    mc.parent(assets,"mmScene_asset_GRP")
    mc.button(AssetsButton,edit=True, enable=False,backgroundColor=(0.025,0.016,0.035))
def ConesPack():
    cones=mc.ls( dag=True, g=1, ap=True, sl=True )      
    mc.select(cones)
    #mc.group(cones,parent="cone_GRP",empty=True)
    mc.parent(cones,"cone_GRP",noConnections=True)
    mc.button(ConesButton,edit=True, enable=False,backgroundColor=(0.025,0.016,0.035))
def HorizonPack():
    Horizon=mc.ls( dag=True, g=1, ap=True, sl=True )         
    mc.select(Horizon)
    mc.parent(Horizon,"wireRed_GRP",noConnections=True)
    mc.button(RedHorizonButton,edit=True, enable=False,backgroundColor=(0.157667,-0.089333,0.351667))
def GreenGeoPack():
    GreenGeo=mc.ls( dag=True, g=1, ap=True, sl=True )        
    mc.select(GreenGeo)
    mc.parent(GreenGeo,"wireGreen_GRP",noConnections=True)
    mc.button(GreenGeoButton,edit=True, enable=False,backgroundColor=(0.221,0.23,-0.211))
def BlueGeoPack():
    BlueGeo=mc.ls( dag=True, g=1, ap=True, sl=True )         
    mc.select(BlueGeo)
    mc.parent(BlueGeo,"wireBlue_GRP",noConnections=True)
    mc.button(BlueGeoButton,edit=True, enable=False,backgroundColor=(-0.254,0.187,0.187))
def YellowGeoPack():
    YellowGeo=mc.ls( dag=True, g=1, ap=True, sl=True )        
    mc.select(YellowGeo)
    mc.parent(YellowGeo,"wireYellow_GRP",noConnections=True)
    mc.button(YellowGeoButton,edit=True, enable=False,backgroundColor=(-0.159,0.057,0.282))
def SphereGridPack():
    SphereGrid=mc.ls( dag=True, g=1, ap=True, sl=True )       
    mc.select(SphereGrid)
    mc.parent(SphereGrid,"sphere_GRP",noConnections=True)
    mc.button(SphereGridButton,edit=True, enable=False,backgroundColor=(-0.105667,0.335333,0.070333))
def Finish():
    mc.deleteUI( IE_FoldersMenu, window=True )



#########################################################################################################################################################################################
#########################################################################################################################################################################################

def mmSceneSetup_createGrps(*args):

    ##mm group template    
    groups = {"mmScene_mmGeo_GRP":[    "cone_GRP",
                                       "sphere_GRP",
                                       "wireRed_GRP",
                                       "wireGreen_GRP",
                                       "wireBlue_GRP",
                                       "wireYellow_GRP"    ],                                            
    
                "mmScene_camera_GRP": [], 
                "mmScene_asset_GRP": []}        
    
    
    ##check scene for exiating groups
    if mc.objExists("ieOSPublish_grp") == True:
        mc.select("ieOSPublish_grp")
        mc.error("error: 'ieOSPublish_grp' already exists.")
    
    
    grpCheck = []
    errorStr = ''
    for k,v in groups.items():
        if mc.objExists(k) == True:
            grpCheck.append(k)
    
    if grpCheck:
        for grp in grpCheck:
            errorStr = errorStr + " '{grp}',".format(grp= grp) 
    #    mc.select(grpCheck)
    #    mc.error("error: '{errorStr}' already exists.".format(errorStr= errorStr))
    
    
    ##create ie OS group hierachy
    ieOSPublish_grp = mc.group(n= "ieOSPublish_grp", em= True)
 
    for k,v in groups.items():
        grp = mc.group(n= k, em= True)
        
        if v:
            for item in v:
                mc.group(n= item, em= True, p= grp)
    
        mc.parent(grp,ieOSPublish_grp) 


    ##lock attrs    
    grps = [ieOSPublish_grp]
    grps.extend(mc.listRelatives(ieOSPublish_grp, c= True, ad= True, f= True))    
    
    for grp in grps:
        atts = mc.listAttr(k= True)
        for att in atts:
            mc.setAttr(grp + "." + att, l = True)
            mc.setAttr(grp + "." + att, k = False)
            mc.setAttr(grp + "." + att, cb = False) 
  
    
    mc.select(ieOSPublish_grp)


#########################################################################################################################################################################################
#########################################################################################################################################################################################


def CreateFolders():
    
    try:
        mmSceneSetup_createGrps()
    except:
        pass
    IE_FoldersMenu()

    try:
        mc.deleteUI( ChooseStudioMenu, window=True )
    except:
        pass   
    
#################################CRAFTY APES #####################################################
##################################################################################################
    

def CreateCamera():
    
    cam = mc.ls(sl=1)[0]
    print (cam)
    
    camShape = mc.listRelatives(cam, c=1)
    print (camShape)
    
    camImage = mc.listRelatives(mc.listConnections(camShape[0]), c=True)
    print (camImage)
    
    
    mc.setAttr(cam +'.tx', lock=1)
    mc.setAttr(cam +'.ty', lock=1)
    mc.setAttr(cam +'.tz', lock=1)
    mc.setAttr(cam +'.rx', lock=1)
    mc.setAttr(cam +'.ry', lock=1)
    mc.setAttr(cam +'.rz', lock=1)
    mc.setAttr(cam +'.sx', lock=1)
    mc.setAttr(cam +'.sy', lock=1)
    mc.setAttr(cam +'.sz', lock=1)
    mc.setAttr(cam +'.v', lock=1)
    mc.setAttr(cam +'.hfa', lock=1)
    mc.setAttr(cam +'.vfa', lock=1)
    mc.setAttr(cam +'.fl', lock=1)
    mc.setAttr(cam +'.lensSqueezeRatio', lock=1)
    mc.setAttr(cam +'.fs', lock=1)
    mc.setAttr(cam +'.fd', lock=1)
    mc.setAttr(cam +'.sa', lock=1)
    mc.setAttr(cam +'.coi', lock=1)
    
    mc.rename(cam,"shotCam")
    mc.rename(camImage,"shotCamPlane")
    try:
        mc.rename("Camera01Trackers","shotCamTrackers")
    except:
        pass
    mc.refresh()

def GroupGeo():

    SelectedGeo = mc.ls(sl=1)
    mc.group(SelectedGeo, n = 'setGeo')
    try:
        mc.ungroup("SynthEyesGroup")
    except:
        pass
    GANS = mc.namespaceInfo(listOnlyNamespaces =True, r=True)
    print (GANS)
    GANS.remove('UI')
    GANS.remove('shared')
    for i in GANS:
        print (i)
        mc.namespace(mnr = 1, rm= i )
    mel.eval("namespaceEditor")


def CraftyStart():
   
    
    global RSwindow
    
    SWwindow = mc.window( title="Cleanup Maya", iconName='CleanUPMaya', w=(600), h=100 )
    mc.columnLayout( adjustableColumn=True )
    mc.text(label='Select Camera then press Camera button. After that select geo(cones,geo,horizon,lidar) \nthen press GroupGeo. Exit at the end\n ',w=200, h=100,rs=1)
    mc.rowLayout(nc=3)
    mc.button(w=200, h=50, label='Camera', command=('CreateCamera()') )
    mc.button(w=200, h=50, label='GroupGeo', command=('GroupGeo()') )
    mc.button(w=200, h=50, label='Exit', command=('mc.deleteUI(\"' + SWwindow + '\", window=True)') )
    mc.setParent( '..' )
    mc.showWindow( SWwindow )

    try:
        mc.deleteUI( ChooseStudioMenu, window=True )
    except:
        pass  



##########################################################TIPPET###########################################
###########################################################################################################

def TippetCamera():
    
    sel_cam=mc.ls(sl=1)
    print (sel_cam)
    
    sel_cam_shape = mc.listRelatives(sel_cam, c=1)
    print (sel_cam_shape)
    
    cam_image = mc.listRelatives(mc.listConnections(sel_cam_shape[0]), c=True)
    print (cam_image)
    
    sel_cam_trns = mc.listRelatives(sel_cam_shape[0], c=1)
    print (sel_cam_trns)
    
    mc.setAttr(sel_cam[0] +".sx",k=0,cb=0)
    mc.setAttr(sel_cam[0] +".sy",k=0,cb=0)
    mc.setAttr(sel_cam[0] +".sz",k=0,cb=0)
    mc.setAttr(sel_cam_shape[0] +".overscan",k=1,l=0,cb=0)
    mc.setAttr(sel_cam_shape[0] +".horizontalFilmOffset",k=1,l=0,cb=0)
    mc.setAttr(sel_cam_shape[0] +".verticalFilmOffset",k=1,l=0,cb=0)
    mc.setAttr(sel_cam_shape[0] +".lsr",k=0,l=0,cb=0)
    mc.setAttr(sel_cam_shape[0] +".fs",k=0,l=0,cb=0)
    mc.setAttr(sel_cam_shape[0] +".fd",k=0,l=0,cb=0)
    mc.setAttr(sel_cam_shape[0] +".sa",k=0,l=0,cb=0)
    mc.setAttr(sel_cam_shape[0] +".coi",k=1,l=0,cb=0)
    mc.setAttr(sel_cam_shape[0] +".coi",100)
    #mc.setAttr(sel_cam_shape[0] +".motion_blur_override",k=0,l=0,cb=0)
    try:
        mc.connectAttr(sel_cam_shape[0] + ".horizontalFilmAperture",cam_image[0] + ".sizeX")
        mc.connectAttr(sel_cam_shape[0] + ".verticalFilmAperture",cam_image[0] + ".sizeY")
    except:
        pass
    mc.setAttr(cam_image[0] + ".alphaGain", 1.0)
    mc.setAttr(cam_image[0] + ".depth", 10000.0)
    mc.rename(sel_cam[0],"mmCam")
    mc.rename(cam_image[0],"bgPlateShape")
    mc.rename(sel_cam_trns,"bgPlate")  
    
    mc.group( em=True, name='mmCamera_N' )
    mc.parent("mmCam",'mmCamera_N')
    
def TippetPackingWindow():
    
    global TPWindow                        
    TPWindow   = mc.window( title="Camera", iconName='Camera', w=(800), h=100 )
    mc.columnLayout( adjustableColumn=True )
    mc.text(label='Select camera to pack Camera, Select geo\lidar to pack geo,Select rig to pack rig, \n Delete everything else ',w=200, h=100,rs=1)
    mc.rowLayout(nc=4)
    mc.button(w=200, h=50, label='Camera', command=('TippetCamera()'))
    mc.button(w=200, h=50, label='Geo', command=('TippetGeo()'))
    mc.button(w=200, h=50, label='Rig', command=('TippetRig()'))
    mc.button(w=200, h=50, label='Exit', command=('cmds.deleteUI(\"' + TPWindow  + '\", window=True)') )
    mc.setParent( '..' )
    mc.showWindow(TPWindow) 

    try:
        mc.deleteUI( ChooseStudioMenu, window=True )
    except:
        pass  

def TippetGeo():
    
    sel_geo=mc.ls(sl=1)
    print (sel_geo)
    
    mc.group( sel_geo, name='mmSet_N' )
    
def TippetRig():
    
    sel_rig=mc.ls(sl=1)
    print (sel_rig)
    mc.group( sel_rig, name='mmStandins_N' )
    mel.eval("namespaceEditor")

#####################################################################################
##################################CHICKENBONE########################################
#####################################################################################            

def ChickenBoneStart():
 
    
    
    
    CBonewindow = mc.window( title="ChickenBone", w=(600), h=100 )
    mc.columnLayout( adjustableColumn=True )
    mc.text(label='Select the items that need renaming and press Start',w=200, h=100,rs=1)
    mc.rowLayout(nc=2)
    mc.button(w=300, h=50, label='Start', command=('CBopt()') )
    mc.button(w=300, h=50, label='Exit', command=('mc.deleteUI(\"' + CBonewindow + '\", window=True)') )
    mc.setParent( '..' )
    mc.showWindow( CBonewindow )
    try:
        mc.deleteUI( ChooseStudioMenu, window=True )
    except:
        pass    
    
def CBopt():
    
    getName = mc.file(q=1,sn=1,shn=1)
    print (getName)
    
    newName = getName.rsplit("main3d")
    print (newName)[0]
    
    prefixNameList = mc.ls(sl=1)
    print (prefixNameList)
    
    for i in range(len(prefixNameList)):
        mc.rename(newName[0] + prefixNameList[i])
        
    mc.ungroup("SynthEyesGroup")
    
    mc.deleteUI( CBonewindow, window=True )
        


ChooseStudio()
              

