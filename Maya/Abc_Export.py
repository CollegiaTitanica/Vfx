import maya.cmds as mc

AbcExport_LOADED = cmds.pluginInfo('AbcExport.mll',q=True,loaded=True)
if not AbcExport_LOADED:
    print("Not Loaded")
    cmds.loadPlugin("AbcExport.mll")
else:
    print("Loaded")

def Find_Create_ABC_Folder():

    FullMayaPath = mc.file(q=True,sn=True)
    MayaFolder = FullMayaPath.split("/")
    print ("FullMayaPath = {}".format(FullMayaPath))
    del MayaFolder[-1]

    

    for MayaFolda in MayaFolder[::-1]:
    
        if MayaFolda != "main3d" :
            MayaFolder.remove(MayaFolda)
        elif MayaFolda == "main3d":
            break
    MayaFolder = "/".join(MayaFolder)
    print ("MayaFolder = {}".format(MayaFolder))
    ABC_Folder = MayaFolder + "/abc/"
    ShotName = MayaFolder.split("/")[-2]
    StudioName = MayaFolder.split("/")[-5]
    print ("ShotName = {}".format(ShotName))
    if not os.path.exists(ABC_Folder):
        original_umask = os.umask(0)
        os.makedirs(ABC_Folder,mode=0o777  )
    return ABC_Folder,ShotName,StudioName

def FindMayaVersion():
    MayaName = mc.file(q=True,sn=True,shn=True)
    SplitMayaName = MayaName.split("_")
    print ("SplitMayaName = {}".format(SplitMayaName))
    for q in reversed(SplitMayaName):
        if "v00" in q:
            return (q)





def ABC_ExportMenu():
    global ABC_ExportMenu
    global CameraButton
    global setGeoButton
    global RigButton   
    global LocatorsButton 
    global SelectAllButton

    ABC_Folder,ShotName,StudioName = Find_Create_ABC_Folder()                
    
    
    if StudioName == "CraftyApes":
        ABC_ExportMenu   = mc.window( title="Abc Export", iconName='Camera', w=(750), h=100 )
        mc.columnLayout( adjustableColumn=True )
        mc.text(label='Select Camera, setGeo , Rigs(if any), Locators (If needed) ',w=200, h=100,rs=1)
        mc.rowLayout(nc=5)
        CameraButton = mc.button(w=150, h=50, label='Camera', command=('SelectCamera()'),backgroundColor=(0.0,1.301644,0.465195))
        setGeoButton = mc.button(w=150, h=50, label='setGeo', command=('SelectsetGeo()'),backgroundColor=(0.680442,0.722698,0.263814))
        RigButton = mc.button(w=150, h=50, label='Rig', command=('SelectRig()'),backgroundColor=(0.270289,0.530539,1.117047))
        LocatorsButton = mc.button(w=150, h=50, label='Locators', command=('SelectLocators()'),backgroundColor=(0.477153,0.064863,0.035372))
        FinishButton = mc.button(w=150, h=50, label='Finish', command=('Finish()') ,backgroundColor=(1.0,0.2,0.3))
    elif StudioName == "Filmlance" or "House_of_Parlament":
        ABC_ExportMenu   = mc.window( title="Abc Export", iconName='Camera', w=(300), h=100 )
        mc.columnLayout( adjustableColumn=True )
        mc.text(label='Select Everything',w=200, h=100,rs=1)
        mc.rowLayout(nc=2)
        SelectAllButton = mc.button(w=150, h=50, label='Everything', command=('SelectAll()'),backgroundColor=(0.680442,0.722698,0.263814))
        FinishButton = mc.button(w=150, h=50, label='Finish', command=('Finish()') ,backgroundColor=(1.0,0.2,0.3))
    mc.setParent( '..' )
    mc.showWindow(ABC_ExportMenu) 


def Abc_Export(filepath,rootlist ,start_frame=1,end_frame=1,data_format='ogawa'):

    
    ABCcommand = '-frameRange {} {} '.format(start_frame,end_frame)
    ABCcommand += '-uvWrite -worldSpace '
    ABCcommand += '-dataFormat {} '.format(data_format)
    for element in rootlist:
       ABCcommand += '-root {} '.format(element) 
    #ABCcommand += '-root {} '.format(root)
    ABCcommand += '-file {} '.format(filepath)

    print ("ABCcommand: {}".format(ABCcommand))
    mc.AbcExport(j=ABCcommand)
#Abc_Export(r'\\fs3\TPN\CraftyApes\WitchesS1\3d_comp\WitchesS1_102_102-020-010_MP_v001\main3d\abc\CAMERA{TEST}.abc',rootlist="shotCam" ,start_frame=1001,end_frame=1088,data_format='ogawa')

#AbcExport -j "-frameRange 1001 1088 -uvWrite -worldSpace -dataFormat ogawa -root |shotCam -file //fs3/TPN/CraftyApes/WitchesS1/3d_comp/WitchesS1_102_102-020-010_MP_v001/main3d/abc/CAMERA{TEST}.abc";

def FindFrameRange():
    startF = int(mc.playbackOptions(min=True, q=True))
    endF = int(mc.playbackOptions(max=True, q=True))
    return startF,endF


def SelectAll():
    ALL=mc.ls(sl=True )
    print(ALL)
    start_frame,end_frame = FindFrameRange()
    ABC_Folder,ShotName,StudioName = Find_Create_ABC_Folder()
    ABC_ALLName = ShotName
    Version = FindMayaVersion()

    ABC_ALLName = ABC_ALLName + Version + ".abc" # Version 
    print ("ABC_ALLName = {}".format(ABC_ALLName))
    Abc_Export(ABC_Folder + ABC_ALLName,rootlist=ALL ,start_frame=start_frame,end_frame=end_frame,data_format='ogawa')
    mc.button(SelectAllButton,edit=True, enable=False,backgroundColor=(-0.578946,0.722698,-0.113751))


def SelectCamera():
    camera=mc.ls(sl=True )
    print(camera)
    start_frame,end_frame = FindFrameRange()
    ABC_Folder,ShotName,StudioName = Find_Create_ABC_Folder()
    ABC_CameraName = ShotName.split("_")
    Version = FindMayaVersion()

    for q in reversed(ABC_CameraName):
        if "v00" in q:
            ABC_CameraName.remove(q)
            break
    ABC_CameraName = "_".join(ABC_CameraName) + "-shotCam_" + Version + ".abc" # Version 
    print ("ABC_CameraName = {}".format(ABC_CameraName))
    Abc_Export(ABC_Folder + ABC_CameraName,rootlist=camera ,start_frame=start_frame,end_frame=end_frame,data_format='ogawa')
    mc.button(CameraButton,edit=True, enable=False,backgroundColor=(-0.578946,0.722698,-0.113751))
def SelectsetGeo():
    setGeo=mc.ls(sl=True )
    print(setGeo)
    start_frame,end_frame = FindFrameRange()
    ABC_Folder,ShotName,StudioName = Find_Create_ABC_Folder()
    ABC_setGeoName = ShotName.split("_")
    Version = FindMayaVersion()

    for q in reversed(ABC_setGeoName):
        if "v00" in q:
            ABC_setGeoName.remove(q)
            break
    ABC_setGeoName = "_".join(ABC_setGeoName) + "-trackGeo_" + Version + ".abc" # Version 
    print ("ABC_setGeoName = {}".format(ABC_setGeoName))
    Abc_Export(ABC_Folder + ABC_setGeoName,rootlist=setGeo ,start_frame=start_frame,end_frame=end_frame,data_format='ogawa')
    mc.button(setGeoButton,edit=True, enable=False,backgroundColor=(0.304791,0.347047,-0.111837))
def SelectRig():
    Rig=mc.ls(sl=True )
    print(Rig)
    start_frame,end_frame = FindFrameRange()
    ABC_Folder,ShotName,StudioName = Find_Create_ABC_Folder()
    ABC_RigName = ShotName.split("_")
    Version = FindMayaVersion()

    for q in reversed(ABC_RigName):
        if "v00" in q:
            ABC_RigName.remove(q)
            break
    ABC_RigName = "_".join(ABC_RigName) + "-trackAnimatedGeo_" + Version + ".abc" # Version 
    print ("ABC_RigName = {}".format(ABC_RigName))
    Abc_Export(ABC_Folder + ABC_RigName,rootlist=Rig ,start_frame=start_frame,end_frame=end_frame,data_format='ogawa')
    mc.button(RigButton,edit=True, enable=False,backgroundColor=(-0.429118,-0.072526,0.501644))  
def SelectLocators():
    Locators=mc.ls(sl=True )
    print(Locators)
    start_frame,end_frame = FindFrameRange()
    ABC_Folder,ShotName,StudioName = Find_Create_ABC_Folder()
    ABC_LocatorsName = ShotName.split("_")
    Version = FindMayaVersion()

    for q in reversed(ABC_LocatorsName):
        if "v00" in q:
            ABC_LocatorsName.remove(q)
            break
    ABC_LocatorsName = "_".join(ABC_LocatorsName) + "-trackLocators_" + Version + ".abc" # Version 
    print ("ABC_LocatorsName = {}".format(ABC_LocatorsName))
    Abc_Export(ABC_Folder + ABC_LocatorsName,rootlist=Locators ,start_frame=start_frame,end_frame=end_frame,data_format='ogawa')
    mc.button(LocatorsButton,edit=True, enable=False,backgroundColor=(0.28469,-0.1276,-0.157091))


def Finish():
    mc.deleteUI( ABC_ExportMenu, window=True )
ABC_ExportMenu()
