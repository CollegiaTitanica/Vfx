import maya.cmds as mc
import re
import os,sys

global Choice
Choice = 1

def Crop_To_Undist(cam):
    #sCam=mc.ls(sl=1)
    CameraName = cam
    sCam = [CameraName]
    #sCam = mc.select (cam)
    print ("sCam = {}".format(sCam))

    sCS = mc.listRelatives(sCam, c=1)
    print ("sCS = {}".format(sCS))

    ipShape = mc.listRelatives(mc.listConnections(sCS[0]), c=True)
    print ("ipShape = {}".format(ipShape))
    DSCam = mc.duplicate(sCam[0])
    #DSCam = mc.duplicate(sCam)


    mc.setAttr(DSCam[0] +".tx", lock=0)
    mc.setAttr(DSCam[0] +".ty", lock=0)
    mc.setAttr(DSCam[0] +".tz", lock=0)
    mc.setAttr(DSCam[0] +".rx", lock=0)
    mc.setAttr(DSCam[0] +".ry", lock=0)
    mc.setAttr(DSCam[0] +".rz", lock=0)

    mc.setAttr(DSCam[0] +".hfa", lock=0)
    mc.setAttr(DSCam[0] +".vfa", lock=0)
    mc.setAttr(DSCam[0] +".fl", lock=0)
    mc.setAttr(DSCam[0] +".lsr", lock=0)
    mc.setAttr(DSCam[0] +".fs", lock=0)
    mc.setAttr(DSCam[0] +".sa", lock=0)
    mc.setAttr(DSCam[0] +".fd", lock=0)
    mc.setAttr(DSCam[0] +".coi", lock=0)
    mc.setAttr(DSCam[0] +".lls", lock=0)

    mc.copyKey(sCam[0])
    mc.pasteKey(DSCam[0])

    FL = mc.getAttr(sCS[0] + ".focalLength")
    mc.setAttr(DSCam[0] + ".focalLength",FL)


    #//fs3/TPN/CraftyApes/Salems/render/Salems_MDF_MDF-028-0110_AP_v001/undist/Salems_MDF_MDF-028-0110_AP_v001_undistort_v001_crop/Salems_MDF_MDF-028-0110_AP_v001_undist_crop.1001.jpg
    UndistCropPlate = mc.getAttr(ipShape[0] + ".imn")
    if type(UndistCropPlate) == list:
        UndistCropPlate = mc.getAttr(ipShape[0] + ".imn")[0]
    
    print ("UndistCropPlate = {}".format(UndistCropPlate))
    UndistFolderSplit = UndistCropPlate.split(".")
    UndistFolderSplit.pop()
    UndistFolderSplit.pop()
    UndistFolderSplit = UndistCropPlate.split("/")
    UndistFolderSplit.pop()
    UndistFolderSplit = "/".join(UndistFolderSplit)
    UndistFolder = UndistFolderSplit.replace("_crop","")
#    UndistFirstImage = os.listdir(UndistFolder)[0]
    UndistList = [x for x in os.listdir(UndistFolder) if x.endswith(".jpg")]
    UndistFirstImage = UndistList[0]
    UndistRealPlate = UndistFolder + "/" + UndistFirstImage
    print ("UndistRealPlate = {}".format(UndistRealPlate))
    print ("UndistFirstImage = {}".format(UndistFirstImage))
    print ("UndistFolderSplit = {}".format(UndistFolderSplit))
    print ("UndistFolder = {}".format(UndistFolder))
    print ("UndistCropPlate = {}".format(UndistCropPlate))

    try:
        mc.imagePlane(fn = UndistRealPlate, camera=DSCam[0])
    except:
        pass

    DSCamShape = mc.listRelatives(DSCam, c=1)
    DSIPShape = mc.listRelatives(mc.listConnections(DSCamShape), c=True)

    mc.select (DSCam)

    mc.setAttr(DSIPShape[0] + ".useFrameExtension", 1)


    cropedX = mc.getAttr(ipShape[0] + ".coverageX")
    if type(cropedX) == list:
        cropedX = mc.getAttr(ipShape[0] + ".coverageX")[0]
    print ("cropedX = {}".format(cropedX))
    origX = mc.getAttr(DSIPShape[0] + ".coverageX")
    print ("origX = {}".format(origX))
    aperaturX = mc.getAttr(sCS[0] + ".horizontalFilmAperture")
    print ("aperaturX = {}".format(aperaturX))               
                    
    cropedY = mc.getAttr(ipShape[0] + ".coverageY")
    if type(cropedY) == list:
        cropedY = mc.getAttr(ipShape[0] + ".coverageY")[0]
    print ("cropedY = {}".format(cropedY))
    origY = mc.getAttr(DSIPShape[0] + ".coverageY")
    print ("origY = {}".format(origY))
    aperaturY = mc.getAttr(sCS[0] + ".verticalFilmAperture")
    print ("aperaturY = {}".format(aperaturY))
                    
    HFA = float(origX) / cropedX * aperaturX
    print ("HFA = {}".format(HFA))
    VFA = float(origY) / cropedY * aperaturY
    print ("VFA = {}".format(VFA))
                    
    mc.setAttr(DSCamShape[0] + ".horizontalFilmAperture", HFA)
    mc.setAttr(DSCamShape[0] + ".verticalFilmAperture", VFA)

    mc.connectAttr(DSCamShape[0] + ".horizontalFilmAperture",DSIPShape[0] + ".sizeX")
    mc.connectAttr(DSCamShape[0] + ".verticalFilmAperture",DSIPShape[0] + ".sizeY")

    mc.setAttr(DSCam[0] +".tx", lock=1)
    mc.setAttr(DSCam[0] +".ty", lock=1)
    mc.setAttr(DSCam[0] +".tz", lock=1)
    mc.setAttr(DSCam[0] +".rx", lock=1)
    mc.setAttr(DSCam[0] +".ry", lock=1)
    mc.setAttr(DSCam[0] +".rz", lock=1)

    mc.setAttr(DSCam[0] +".hfa", lock=1)
    mc.setAttr(DSCam[0] +".vfa", lock=1)
    mc.setAttr(DSCam[0] +".fl", lock=1)
    mc.setAttr(DSCam[0] +".lsr", lock=1)
    mc.setAttr(DSCam[0] +".fs", lock=1)
    mc.setAttr(DSCam[0] +".sa", lock=1)
    mc.setAttr(DSCam[0] +".fd", lock=1)
    mc.setAttr(DSCam[0] +".coi", lock=1)
    mc.setAttr(DSCam[0] +".lls", lock=1)

    mc.setAttr(DSIPShape[0] + ".depth", 10000)

    try:
        if "_crop".lower() in DSCam[0]:
            mc.rename(DSCam[0],DSCam[0].replace("_crop",""))
            print ("Crop")
        else:
            mc.rename(DSCam[0],"UndistCamera")
            print ("Except")
    except:
        pass

    cmds.setAttr(DSIPShape[0] + ".fit",4)



def Undist_To_Crop(cam):
    global BASE_DIR

    def set_BASE_DIR(base_dir):
        global BASE_DIR
        BASE_DIR = base_dir

    def undist_plates(cam_ip):

        undistPlates_path = cmds.getAttr(cam_ip + ".imn")
        print ("undistPlates_path = {}".format(undistPlates_path))

        first_frame_numbers = undistPlates_path.split('.')[-2]
        print ("first_frame_numbers = {}".format(first_frame_numbers))

        undist_base_folder_path = undistPlates_path.split('/undist/')[0] + '/undist/'
        print ("undist_base_folder_path = {}".format(undist_base_folder_path))
        undist_folder_path = undistPlates_path.split('/undist/')[1]
        print ("undist_folder_path = {}".format(undist_folder_path))
        undist_folder_name = undist_folder_path.split('/')[0]
        print ("undist_folder_name = {}".format(undist_folder_name))
        undist_crop_folder_name = undist_folder_name + '_crop'
        print ("undist_crop_folder_name = {}".format(undist_crop_folder_name))
        
        typeImage = undistPlates_path.split('.')[-1]
        print ("typeImage = {}".format(typeImage))

        UndistCropPath = undist_base_folder_path + undist_crop_folder_name
        try:
            FirstCrop = os.listdir(UndistCropPath)[0]
            print ("FirstCrop = {}".format(FirstCrop))
        except WindowsError:
            cmds.confirmDialog(title="ERROR:",message="Cannot find crop folder. It should end with '_undist_crop'",button=["I'm sorry :("],defaultButton="I'm sorry :(")
            # cmds.error("Cannot find crop folder. It should end with '_undist_crop'")
        except IndexError:
            cmds.confirmDialog(title="ERROR:",message="Crop folder is empty. Shame on you",button=["I'm sorry :("],defaultButton="I'm sorry :(")
        try:
            undist_crop_plates_path = undist_base_folder_path + undist_crop_folder_name + '/' + FirstCrop
            print ("undist_crop_plates_path = {}".format(undist_crop_plates_path))

            RAW_undist_crop_plates_path = r"{}".format(undist_crop_plates_path)
            print ("RAW_undist_crop_plates_path = {}".format(RAW_undist_crop_plates_path))
            return RAW_undist_crop_plates_path
            
        except:
            return None
            pass

    def Create_Crop(cam):
        cam_shape = cmds.listRelatives(cam, c=1)[0]
        print ("cam_shape = {}".format(cam_shape))
        cam_ip = cmds.listRelatives(cmds.listConnections(cam_shape, c=True))[0]
        print ("cam_ip = {}".format(cam_ip))
    
        CropPath = undist_plates(cam_ip)
        print ("CropPath = {}".format(CropPath))

        # If crop path is found and not empty; Proceed, otherwise stop
        if CropPath != None:
            LoadCamera(cam, CropPath,cam_shape,cam_ip)
      
    def LoadCamera(cam,CropPath,cam_shape,cam_ip):
        # export import
        cmds.file(BASE_DIR + "include_scripts/WR_tmp_cam/tmpCam.ma", es=True, f=True,
                typ="mayaAscii")
        cmds.file(BASE_DIR + "include_scripts/WR_tmp_cam/tmpCam.ma", i=True, ra=True,
                rpr="crop", pr=False, mnc=False, op="v=0;")

        CamParentFound = False
        try:
            cam_parent = cmds.listRelatives(cam, p=1)[0]
            print ("cam_parent = {}".format(cam_parent))
            CamParentFound = True
            print ("CamParentFound = {}".format(CamParentFound))
        except:
            CamParentFound = False
            print ("CamParentFound = {}".format(CamParentFound))
        # reparent
        if CamParentFound:
            print ("CamPARENT FOUND")
            cmds.parent("crop_" + cam, cam_parent)
            cmds.rename("crop_" + cam, cam + "_crop")
            cmds.delete("crop_" + cam_parent)
        else:
            cmds.rename("crop_" + cam, cam + "_crop")

        cam_crop = cam + "_crop"
        cam_crop_shape = cmds.listRelatives(cam_crop, c=1)[0]
        EX_cam_crop_ip = cmds.listRelatives(cmds.listConnections(cam_crop_shape, c=True))
        print ("EX_cam_crop_ip = {}".format(EX_cam_crop_ip))

        imagePlaneList = cmds.listConnections("{}.imagePlane".format(cam_crop_shape),type="imagePlane",et=True)
        imagePlane = imagePlaneList[0]
        print ("imagePlaneList = {}".format(imagePlaneList))
        print ("imagePlane = {}".format(imagePlane))

        AllConnections_IP = mc.listConnections(cam_crop_shape)
       # cam_crop_ip = mc.listConnections(cam_crop_shape)[0]
        cam_crop_ip = imagePlane
        print ("cam_crop_ip = {}".format(cam_crop_ip))
        print ("AllConnections_IP = {}".format(AllConnections_IP))
        # set image planes for camera_crop
        if os.path.exists(undist_plates(cam_ip)[0]):
            cmds.setAttr(cam_crop_ip + ".imn", CropPath, type="string")

        cmds.setAttr(cam_crop_ip + ".useFrameExtension", 1)

        cmds.refresh()

        # set aperture settings
        cropedX = cmds.getAttr(cam_crop_ip + ".coverageX")
        origX = cmds.getAttr(cam_ip + ".coverageX")
        apertureX = cmds.getAttr(cam_shape + ".horizontalFilmAperture")

        cropedY = cmds.getAttr(cam_crop_ip + ".coverageY")
        origY = cmds.getAttr(cam_ip + ".coverageY")
        apertureY = cmds.getAttr(cam_shape + ".verticalFilmAperture")

        HFA = float(cropedX) / origX * apertureX
        VFA = float(cropedY) / origY * apertureY
        print ("HFA = {}".format(HFA))
        print ("VFA = {}".format(VFA))
        
        cmds.setAttr(cam_crop_shape + ".hfa", lock=False)
        cmds.setAttr(cam_crop_shape + ".horizontalFilmAperture", HFA)
        cmds.setAttr(cam_crop_shape + ".hfa", lock=True)

        cmds.setAttr(cam_crop_shape + ".vfa", lock=False)
        cmds.setAttr(cam_crop_shape + ".verticalFilmAperture", VFA)
        cmds.setAttr(cam_crop_shape + ".vfa", lock=True)
        try:
            mc.connectAttr(cam_crop_shape + ".horizontalFilmAperture",cam_crop_ip + ".sizeX")
            mc.connectAttr(cam_crop_shape + ".verticalFilmAperture",cam_crop_ip + ".sizeY")
        except:
            pass
#        try:
#            cmds.setAttr(cam_crop_ip + ".sizeX", HFA)
#            cmds.setAttr(cam_crop_ip + ".sizeY", VFA)
#        except:
#            print("Failed")
#            pass

    Create_Crop(cam)
    #def camera_crop_main():
        

        


   # camera_crop_main()

def TimeToChooseMrFreeman(Number):
    global Choice
    Choice = Number

def CameraChoice(*args):
    global Choice

    if Choice == 1:
        try:
            cam = cmds.ls(sl=1)[0]
            cam_shape = cmds.listRelatives(cam, c=1)[0]
            if (cmds.objectType(cam_shape) == 'camera'):
                Undist_To_Crop(cam)
            else:
                cmds.confirmDialog(title="ERROR:",message="Camera not Selected",button=["I'm sorry :("],defaultButton="I'm sorry :(")
        except IndexError:
            cmds.confirmDialog(title="ERROR:",message="Nothing Selected!",button=["I'm sorry :("],defaultButton="I'm sorry :(")
        print("Choice == 1") 
    elif Choice == 2:
        try:
            cam = cmds.ls(sl=1)[0]
            cam_shape = cmds.listRelatives(cam, c=1)[0]
            if (cmds.objectType(cam_shape) == 'camera'):
                Crop_To_Undist(cam)
            else:
                cmds.confirmDialog(title="ERROR:",message="Camera not Selected",button=["I'm sorry :("],defaultButton="I'm sorry :(")
        except IndexError:
            cmds.confirmDialog(title="ERROR:",message="Nothing Selected!",button=["I'm sorry :("],defaultButton="I'm sorry :(")
        print("Choice == 2") 
    else:
        mc.error("No Mode Selected")




UNCWindow = mc.window( title="Undist To Crop", iconName='RS', w=(400), h=100 )
mc.columnLayout( adjustableColumn=True )
mc.text(label='Select the Camera, then choose what operation you wish to perform on it.',w=150, h=50,rs=1)
mc.rowLayout(nc=2)
mc.rowColumnLayout(nc=2)
mc.radioCollection()
Undist_To_Crop_Radio = mc.radioButton(label='Undist To Crop',select=True, onCommand=lambda x:TimeToChooseMrFreeman(1))
Crop_To_Undist_Radio = mc.radioButton(label='Crop to Undist', onCommand=lambda x:TimeToChooseMrFreeman(2))

mc.button(w=200, h=50, label='Execute', command=CameraChoice )
mc.setParent( '..' )
mc.showWindow( UNCWindow )