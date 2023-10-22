import os
import sys
import nuke
import nukescripts
import shutil
import threading

#ThreeD_comp_Path = r"\\fs3\TPN\Tippett\SWC\3d_comp\101_002_0150_bg_original_v002_acescg"
#ThreeD_comp_Path = r"\\fs3\TPN\Tippett\JAM_RTR\3d_comp\sch_2002_bg_original01_v001_aces"
#render_Path = r"\\fs3\TPN\Tippett\SWC\render\101_002_0150_bg_original_v002_acescg"
#render_Path = r"\\fs3\TPN\Tippett\JAM_RTR\render\sch_2002_bg_original01_v001_aces"
#jpg_Path = r"\\fs3\TPN\Tippett\SWC\input\Vertigo_Tippett_SWC_20230302_MM_plates\230223_plates_101_002\101_002_0150\plates\bg\original\v002\jpg"
#jpg_Path = r"\\fs3\TPN\Tippett\JAM_RTR\input\Vertigo_Tippett_JAM_20221222\sch_2002\plates\bg\original01\v001\jpg"
#Version = "v001"
#ShotName = "101_002_0150_bg_original_v002_acescg"
#ShotName = "sch_2002_bg_original01_v001_aces"

############
#PIS_Status = "Source"
#PIS_Status = "Undist"
#PIS_Status = "Crop"
############


def Nuke_Preview(ShotName, ThreeD_comp_Path,render_Path,jpg_Path,Version,PIS_Status,UV_LD_Status):

    def GetPadding():
        try:
            for image in os.listdir(jpg_Path):
                Split = image.split(".")
                Split.pop()
                Split = Split[-1]
                NumberCount = 0
                for l in Split:
                    NumberCount += 1
            
                return NumberCount
        except FileNotFoundError:
            nuke.message("JPG not Found!")
          #  sys.exit()

    Padding = GetPadding()
    Taraba = ""

    for t in range(Padding):
        Taraba += "#"
    print ("Taraba = {}".format(Taraba)) 

    global LDCheck
    LDCheck = False



    for a in nuke.allNodes():
        nuke.delete(a)
        
    try:
        LDNodePath = ThreeD_comp_Path +  "\\nuke\\"
    except:
        if not os.path.exists(LDNodePath):
            original_umask = os.umask(0)
            os.makedirs(LDNodePath,mode=0o777  ) 
        pass
    try:
        for LD in os.listdir(LDNodePath):
            if "dist_".lower() in LD.lower():
                Split,ext = os.path.splitext(LD)
                SplitDist = Split.split("_")
                for v in SplitDist:
                    if "v0" in v:
                        LastVersion = v
                        
        try:
            LastVersion
        except NameError:
            LastVersion = None
            pass
        for LD in os.listdir(LDNodePath):
            try:
                if "dist_{}".format(LastVersion).lower() in LD.lower():
                        LDCheck = True
                        print ("LD Node Found")
#                else:
#                    LDCheck = False
            except:
                pass
    except:
        pass


    LDNodePath = ThreeD_comp_Path +  "\\nuke\\"
    
    TippettPath = r"\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\\"
    ProjectPath = render_Path.split("\\")[:-2]
    ProjectName = ProjectPath[-1]
    StudioName = ProjectPath[-2]
    ProjectPath = "/".join(ProjectPath)
    print ("ProjectPath = {}".format(ProjectPath))
    print ("ProjectName = {}".format(ProjectName))
    print ("StudioName = {}".format(StudioName))
    #####################################################
    OriginalUndistPath=render_Path + "\\undist" + "\\"
    OriginalUndistPath=OriginalUndistPath.replace("\\","/")
    UndistFolder=os.listdir(OriginalUndistPath)
    for folders in UndistFolder:
        SplitFolderName= folders.split("_")
        Reversed_SplitFolderName = reversed(SplitFolderName)
        print ("OriginalSplitFolderName = {}".format(SplitFolderName))
        LastSLOG = SplitFolderName[-1]
    #    UndistFolderName="_".join(SplitFolderName)
        if LastSLOG=="undist" or LastSLOG =="undistorted" or LastSLOG == "undistort":
            for index,v in enumerate(Reversed_SplitFolderName):
                if LastSLOG=="undist" or LastSLOG =="undistorted" or LastSLOG == "undistort":
                    if "v00" in v:
                        (SplitFolderName[-index-1]) = Version
                        break

                UndistFolderName="_".join(SplitFolderName)
            print ("UndistFolderName         = {}".format(UndistFolderName))
            print ("LastSLOG         = {}".format(LastSLOG))
            print ("SplitFolderName         = {}".format(SplitFolderName))
    
    if PIS_Status == "Undist":
        try:
            UndistPath=render_Path + "\\undist\\"
            UndistPath=UndistPath.replace("\\","/")
            UndistPath+=UndistFolderName + "\\"     
            Continue_Preview(ShotName, ThreeD_comp_Path,render_Path,jpg_Path,Version,PIS_Status,UV_LD_Status,Taraba,LDCheck,LDNodePath,TippettPath,ProjectName,StudioName,LastVersion,UndistPath)
        except UnboundLocalError:
            nuke.message("""Missing Undist! Undist Folder should end with '_undist' """)
            #nuke.scriptExit()
            

            
    elif PIS_Status == "Crop":
        try:    
            CropPath = OriginalUndistPath + "{}".format(UndistFolderName) + "_crop" + "/"
            Continue_Preview(ShotName, ThreeD_comp_Path,render_Path,jpg_Path,Version,PIS_Status,UV_LD_Status,Taraba,LDCheck,LDNodePath,TippettPath,ProjectName,StudioName,LastVersion,CropPath)
        except UnboundLocalError:
            nuke.message("""Missing Undist! Undist Folder should end with '_undist' """)
            #nuke.scriptExit()
            
    elif PIS_Status == "Source":
        Continue_Preview(ShotName, ThreeD_comp_Path,render_Path,jpg_Path,Version,PIS_Status,UV_LD_Status,Taraba,LDCheck,LDNodePath,TippettPath,ProjectName,StudioName,LastVersion,None)

    try:
        if PIS_Status == "Crop" and not os.path.exists(CropPath):
            nuke.message("""Missing Crop! Crop Folder should end with '_undist_crop' and Undist Folder should end with '_undist'""")
            #nuke.scriptExit()
            
    except:
        pass



def Continue_Preview(ShotName, ThreeD_comp_Path,render_Path,jpg_Path,Version,PIS_Status,UV_LD_Status,Taraba,LDCheck,LDNodePath,TippettPath,ProjectName,StudioName,LastVersion,PIS_Path):

    global Cones_Check
    global Geo_Check
    global Rig_Check
    global Rig1_Check
    global Rig2_Check
    global Rig3_Check
    global Rig4_Check
    global Rig5_Check
    global TransformNodes
    global Lidar_Check
    global Lidar1_Check
    global Lidar2_Check
    global Anamorphic
    Cones_Check = False
    Geo_Check = False
    Lidar_Check = False
    Lidar1_Check = False
    Lidar2_Check = False
    Rig_Check = False
    Rig1_Check = False
    Rig2_Check = False
    Rig3_Check = False
    Rig4_Check = False
    Rig5_Check = False
    Anamorphic = False

    TransformNodes = []


    #####################################################
    ####   Determine which image sequence should be utilized at the bottom depending on PIS_Status (Source,Undist,Crop)
    if PIS_Status == "Source":
        JPGPath=jpg_Path + "\\"
        JPGPath=JPGPath.replace("\\","/")
        print ("JPGPath = {}".format(JPGPath))                  
    elif PIS_Status == "Undist":
        try:
            JPGPath = PIS_Path          #UndistPath
        except:
            pass
    elif PIS_Status == "Crop":
        try:
            JPGPath = PIS_Path          #CropPath
        except:
            pass
                 

    UVDistortPath=render_Path + "\\uvmap\\"
    UVDistortPath=UVDistortPath.replace("\\","/")
    print ("UVDistortPath = {}".format(UVDistortPath))
    RealPreviewFolder = []
    OriginalPreviewPath=render_Path + "\\preview\\"
    print ("OriginalPreviewPath = {}".format(OriginalPreviewPath))
#              OriginalPreviewPath=OriginalPreviewPath.replace("\\","/")
#             os.listdir(OriginalPreviewPath)
    for folder in os.listdir(OriginalPreviewPath):
        print (folder)
        FolderName = folder.split("_")
        FolderNameNext = folder.split("_")
        print ("FolderName = {}".format(FolderName))
        ReversedFolderName = list(reversed(FolderName))
        ReversedFolderNameNext = list(reversed(FolderName))
        print ("ReversedFolderName = {}".format(ReversedFolderName))

    for n in ReversedFolderName:
        if "v00" in n:
            
            if n == Version:
                print("True")
                RealPreviewFolder.append(folder)
                PreviewPath = OriginalPreviewPath + folder + "\\"
                PreviewPath = PreviewPath.replace("\\","/")
                print ("PreviewPath = {}".format(PreviewPath))
                print ("First Time")

            else:
                for item,k in enumerate(ReversedFolderNameNext):
                    if "v00" in k:
                        ReversedFolderNameNext[item]=Version
                        ReversedFolderNameNext = list(reversed(ReversedFolderNameNext))
                        FolderJoin="_".join(ReversedFolderNameNext)
                        print ("FolderJoin = {}".format(FolderJoin))
                        print ("ReversedFolderNameNext = {}".format(ReversedFolderNameNext))
                        if not os.path.exists(OriginalPreviewPath + "\\" + FolderJoin):
                            os.makedirs(OriginalPreviewPath + "\\" + FolderJoin) 
                        RealPreviewFolder.append(FolderJoin)
                        PreviewPath = OriginalPreviewPath + FolderJoin + "\\"
                        PreviewPath = PreviewPath.replace("\\","/")
                        print ("PreviewPath = {}".format(PreviewPath))
                        print ("Second Time")
                        break

            break
    try:
        LidarCheckFile = ThreeD_comp_Path + "/main3d/" + "LidarCheck.txt"
        for lidarfile in os.listdir(ThreeD_comp_Path + "/main3d/"):
            if lidarfile == "LidarCheck.txt":
                Lidar_Check=True


    except:
        pass
    print ("RealPreviewFolder = {}".format(RealPreviewFolder))
    Main3dPath = render_Path + "/main3d/" + Version + "/"
    Main3dPath = Main3dPath.replace("\\","/")
    print ("Main3dPath = {}".format(Main3dPath)) 
    if StudioName == "ImageEngine":
        GeoPath=Main3dPath + "LIDAR/"
        GeoPath=GeoPath.replace("\\","/")
        print ("GeoPath = {}".format(GeoPath))
    else:    
        GeoPath=Main3dPath + "GEO/"
        GeoPath=GeoPath.replace("\\","/")
        print ("GeoPath = {}".format(GeoPath))
    RigPath=Main3dPath + "RIG/"
    RigPath=RigPath.replace("\\","/")
    print ("RigPath = {}".format(RigPath))
###
    LidarPath=Main3dPath + "LIDAR/"
    LidarPath=LidarPath.replace("\\","/")
    print ("LidarPath = {}".format(LidarPath))
    Lidar1Path=Main3dPath + "LIDAR1/"
    Lidar1Path=Lidar1Path.replace("\\","/")
    print ("Lidar1Path = {}".format(Lidar1Path))
    Lidar2Path=Main3dPath + "LIDAR2/"
    Lidar2Path=Lidar2Path.replace("\\","/")
    print ("Lidar2Path = {}".format(Lidar2Path))
###
    Rig1Path=Main3dPath + "RIG1/"
    Rig1Path=Rig1Path.replace("\\","/")
    print ("Rig1Path = {}".format(Rig1Path))
    Rig2Path=Main3dPath + "RIG2/"
    Rig2Path=Rig2Path.replace("\\","/")
    print ("Rig2Path = {}".format(Rig2Path))
    Rig3Path=Main3dPath + "RIG3/"
    Rig3Path=Rig3Path.replace("\\","/")
    print ("Rig3Path = {}".format(Rig3Path))
    Rig4Path=Main3dPath + "RIG4/"
    Rig4Path=Rig4Path.replace("\\","/")
    print ("Rig4Path = {}".format(Rig4Path))
    Rig5Path=Main3dPath + "RIG5/"
    Rig5Path=Rig5Path.replace("\\","/")
    print ("Rig5Path = {}".format(Rig5Path))
###
    ConesPath=Main3dPath + "CONES/"
    ConesPath=ConesPath.replace("\\","/")
    print ("ConesPath = {}".format(ConesPath))

    # 3d_Comp:
    SaveNukePreviewPath = "{}".format(ThreeD_comp_Path) +"\\preview\\"
    print ("SaveNukePreviewPath = {}".format(SaveNukePreviewPath))
    if not os.path.exists(SaveNukePreviewPath):
        original_umask = os.umask(0)
        os.makedirs(SaveNukePreviewPath,mode=0o777  ) 

    def CreateTree(Tree="Cones",red=1,green=0,blue=1,mix=1,gamma=1.0):
        global Cones_Check
        global Geo_Check
        global Rig_Check
        global Rig1_Check
        global Rig2_Check
        global Rig3_Check
        global Rig4_Check
        global Rig5_Check
        global Anamorphic
        if Tree == "Cones":
            Cones_Check = True
            print ("Cones_Check = {}".format(Cones_Check))     
            for seq in nuke.getFileNameList(ConesPath):
                CreateTree.ConesReadNode = nuke.nodes.Read()
                CreateTree.ConesReadNode.knob('file').fromUserText(ConesPath + seq)
                CreateTree.ConesReadNode['label'].setValue(Tree)
                CreateTree.ConesTransformNode = nuke.createNode("Transform")
                CreateTree.ConesTransformNode.setInput(0,CreateTree.ConesReadNode)
                CreateTree.ConesTransformNode.setXYpos(CreateTree.ConesReadNode.xpos(),CreateTree.ConesReadNode.ypos()+100)
                TransformNodes.append(CreateTree.ConesTransformNode)
                CreateTree.ConesShuffleNode = nuke.createNode('Shuffle')
                CreateTree.ConesShuffleNode['alpha'].setValue('red')
                CreateTree.ConesShuffleNode.setInput(0,CreateTree.ConesTransformNode)
                CreateTree.ConesShuffleNode.setXYpos(CreateTree.ConesTransformNode.xpos(),CreateTree.ConesTransformNode.ypos()+40)
#                CreateTree.ConesReadNode["xpos"].setValue(CreateTree.ConesShuffleNode.xpos())
#                CreateTree.ConesReadNode["ypos"].setValue(CreateTree.ConesShuffleNode.ypos()-140)
                
                CreateTree.ConesColorCorrectNode = nuke.createNode('ColorCorrect')
                CreateTree.ConesColorCorrectNode.knob('gamma').setValue(gamma)
                CreateTree.ConesColorCorrectNode.knob('gain').setValue(red,0)    #RED
                CreateTree.ConesColorCorrectNode.knob('gain').setValue(green,1)    #GREEN
                CreateTree.ConesColorCorrectNode.knob('gain').setValue(blue,2)    #BLUE
                CreateTree.ConesColorCorrectNode.knob('gain').setValue(1,3)    #ALPHA
                CreateTree.ConesColorCorrectNode.setXYpos(CreateTree.ConesShuffleNode.xpos(),CreateTree.ConesShuffleNode.ypos()+40)
                CreateTree.ConesBlurNode = nuke.createNode('Blur')
                CreateTree.ConesBlurNode['disable'].setValue(True)
                CreateTree.ConesBlurNode["size"].setValue(1.2,0)
                CreateTree.ConesBlurNode.setXYpos(CreateTree.ConesColorCorrectNode.xpos(),CreateTree.ConesColorCorrectNode.ypos()+40)
                CreateTree.ConesErodeNode = nuke.createNode("Dilate")
                CreateTree.ConesErodeNode["size"].setValue(0.5)
                CreateTree.ConesErodeNode['disable'].setValue(True)
                CreateTree.ConesErodeNode.setXYpos(CreateTree.ConesBlurNode.xpos(),CreateTree.ConesBlurNode.ypos()+40)
                CreateTree.ConesMergeNode = nuke.nodes.Merge2()
                CreateTree.ConesMergeNode.setInput(1, CreateTree.ConesErodeNode)
                CreateTree.ConesMergeNode['label'].setValue(Tree)
                CreateTree.ConesMergeNode.setXYpos(CreateTree.ConesErodeNode.xpos(),CreateTree.ConesErodeNode.ypos()+80)
                CreateTree.ConesMergeNode['selected'].setValue(False)
                for w in nuke.allNodes():
                    w.setSelected(False)
        elif Tree == "Geo":
            Geo_Check = True
            print ("Geo_Check = {}".format(Geo_Check))   
            for seq in nuke.getFileNameList(GeoPath):
                CreateTree.GeoReadNode = nuke.nodes.Read()
                CreateTree.GeoReadNode.knob('file').fromUserText(GeoPath + seq)
                CreateTree.GeoReadNode['label'].setValue(Tree)
                CreateTree.GeoTransformNode = nuke.createNode("Transform")
                CreateTree.GeoTransformNode.setInput(0,CreateTree.GeoReadNode)
                TransformNodes.append(CreateTree.GeoTransformNode)
                CreateTree.GeoShuffleNode = nuke.createNode('Shuffle')
                CreateTree.GeoShuffleNode['alpha'].setValue('red')
                CreateTree.GeoShuffleNode.setInput(0,CreateTree.GeoTransformNode)
                CreateTree.GeoShuffleNode.setXYpos(CreateTree.GeoTransformNode.xpos(),CreateTree.GeoTransformNode.ypos()+40)
                try:
                    if StudioName == "ImageEngine":
                        CreateTree.GeoReadNode["xpos"].setValue(CreateTree.ConesReadNode.xpos()+750)
                        CreateTree.GeoReadNode["ypos"].setValue(CreateTree.ConesReadNode.ypos())
                    else:
                        CreateTree.GeoReadNode["xpos"].setValue(CreateTree.ConesReadNode.xpos()+350)
                        CreateTree.GeoReadNode["ypos"].setValue(CreateTree.ConesReadNode.ypos())
                except:
                    pass
                CreateTree.GeoTransformNode.setXYpos(CreateTree.GeoReadNode.xpos(),CreateTree.GeoReadNode.ypos()+100)
                CreateTree.GeoShuffleNode.setXYpos(CreateTree.GeoReadNode.xpos(),CreateTree.GeoReadNode.ypos()+140)
                CreateTree.GeoColorCorrectNode = nuke.createNode('ColorCorrect')
                CreateTree.GeoColorCorrectNode.knob('gamma').setValue(gamma)
                CreateTree.GeoColorCorrectNode.knob('gain').setValue(red,0)    #RED
                CreateTree.GeoColorCorrectNode.knob('gain').setValue(green,1)    #GREEN
                CreateTree.GeoColorCorrectNode.knob('gain').setValue(blue,2)    #BLUE
                CreateTree.GeoColorCorrectNode.knob('gain').setValue(1,3)    #ALPHA
                CreateTree.GeoColorCorrectNode.setXYpos(CreateTree.GeoShuffleNode.xpos(),CreateTree.GeoShuffleNode.ypos()+40)
                CreateTree.GeoBlurNode = nuke.createNode('Blur')
                CreateTree.GeoBlurNode['disable'].setValue(True)
                CreateTree.GeoBlurNode["size"].setValue(1.2,0)
                CreateTree.GeoBlurNode.setXYpos(CreateTree.GeoColorCorrectNode.xpos(),CreateTree.GeoColorCorrectNode.ypos()+40)
                CreateTree.GeoErodeNode = nuke.createNode("Dilate")
                CreateTree.GeoErodeNode["size"].setValue(0.5)
                CreateTree.GeoErodeNode['disable'].setValue(True)
                CreateTree.GeoErodeNode.setXYpos(CreateTree.GeoBlurNode.xpos(),CreateTree.GeoBlurNode.ypos()+40)
                CreateTree.GeoMergeNode = nuke.nodes.Merge2()
                CreateTree.GeoMergeNode.setInput(1, CreateTree.GeoErodeNode)
                CreateTree.GeoMergeNode['label'].setValue(Tree)
                CreateTree.GeoMergeNode.setXYpos(CreateTree.GeoErodeNode.xpos(),CreateTree.GeoErodeNode.ypos()+80)
                CreateTree.GeoMergeNode['selected'].setValue(False)
                CreateTree.GeoMergeNode.knob('mix').setValue(mix)
                for w in nuke.allNodes():
                    w.setSelected(False)
        elif Tree == "Lidar":
            global Lidar_Check
            Lidar_Check = True
            print ("Lidar_Check = {}".format(Lidar_Check))   
            for seq in nuke.getFileNameList(LidarPath):
                CreateTree.LidarReadNode = nuke.nodes.Read()
                CreateTree.LidarReadNode.knob('file').fromUserText(LidarPath + seq)
                CreateTree.LidarReadNode['label'].setValue(Tree)
                CreateTree.LidarTransformNode = nuke.createNode("Transform")
                CreateTree.LidarTransformNode.setInput(0,CreateTree.LidarReadNode)
                TransformNodes.append(CreateTree.LidarTransformNode)
                CreateTree.LidarShuffleNode = nuke.createNode('Shuffle')
                CreateTree.LidarShuffleNode['alpha'].setValue('red')
                CreateTree.LidarShuffleNode.setInput(0,CreateTree.LidarTransformNode)
                CreateTree.LidarShuffleNode.setXYpos(CreateTree.LidarTransformNode.xpos(),CreateTree.LidarTransformNode.ypos()+40)
                try:
                    if StudioName == "ImageEngine":
                        CreateTree.LidarReadNode["xpos"].setValue(CreateTree.ConesReadNode.xpos()-550)
                        CreateTree.LidarReadNode["ypos"].setValue(CreateTree.ConesReadNode.ypos())
                    else:
                        CreateTree.LidarReadNode["xpos"].setValue(CreateTree.ConesReadNode.xpos()-350)
                        CreateTree.LidarReadNode["ypos"].setValue(CreateTree.ConesReadNode.ypos())
                except:
                    pass
                CreateTree.LidarTransformNode.setXYpos(CreateTree.LidarReadNode.xpos(),CreateTree.LidarReadNode.ypos()+100)
                CreateTree.LidarShuffleNode.setXYpos(CreateTree.LidarReadNode.xpos(),CreateTree.LidarReadNode.ypos()+140)
                CreateTree.LidarColorCorrectNode = nuke.createNode('ColorCorrect')
                CreateTree.LidarColorCorrectNode.knob('gamma').setValue(gamma)
                CreateTree.LidarColorCorrectNode.knob('gain').setValue(red,0)    #RED
                CreateTree.LidarColorCorrectNode.knob('gain').setValue(green,1)    #GREEN
                CreateTree.LidarColorCorrectNode.knob('gain').setValue(blue,2)    #BLUE
                CreateTree.LidarColorCorrectNode.knob('gain').setValue(1,3)    #ALPHA
                CreateTree.LidarColorCorrectNode.setXYpos(CreateTree.LidarShuffleNode.xpos(),CreateTree.LidarShuffleNode.ypos()+40)
                CreateTree.LidarBlurNode = nuke.createNode('Blur')
                CreateTree.LidarBlurNode['disable'].setValue(True)
                CreateTree.LidarBlurNode["size"].setValue(1.2,0)
                CreateTree.LidarBlurNode.setXYpos(CreateTree.LidarColorCorrectNode.xpos(),CreateTree.LidarColorCorrectNode.ypos()+40)
                CreateTree.LidarErodeNode = nuke.createNode("Dilate")
                CreateTree.LidarErodeNode["size"].setValue(0.5)
                CreateTree.LidarErodeNode['disable'].setValue(True)
                CreateTree.LidarErodeNode.setXYpos(CreateTree.LidarBlurNode.xpos(),CreateTree.LidarBlurNode.ypos()+40)
                CreateTree.LidarMergeNode = nuke.nodes.Merge2()
                CreateTree.LidarMergeNode.setInput(1, CreateTree.LidarErodeNode)
                CreateTree.LidarMergeNode['label'].setValue(Tree)
                CreateTree.LidarMergeNode.setXYpos(CreateTree.LidarErodeNode.xpos(),CreateTree.LidarErodeNode.ypos()+80)
                CreateTree.LidarMergeNode['selected'].setValue(False)
                CreateTree.LidarMergeNode.knob('mix').setValue(mix)
                for w in nuke.allNodes():
                    w.setSelected(False)
        elif Tree == "Lidar1":
            global Lidar1_Check
            Lidar1_Check = True
            print ("Lidar1_Check = {}".format(Lidar1_Check))   
            for seq in nuke.getFileNameList(Lidar1Path):
                CreateTree.Lidar1ReadNode = nuke.nodes.Read()
                CreateTree.Lidar1ReadNode.knob('file').fromUserText(Lidar1Path + seq)
                CreateTree.Lidar1ReadNode['label'].setValue(Tree)
                CreateTree.Lidar1TransformNode = nuke.createNode("Transform")
                CreateTree.Lidar1TransformNode.setInput(0,CreateTree.Lidar1ReadNode)
                TransformNodes.append(CreateTree.Lidar1TransformNode)
                CreateTree.Lidar1ShuffleNode = nuke.createNode('Shuffle')
                CreateTree.Lidar1ShuffleNode['alpha'].setValue('red')
                CreateTree.Lidar1ShuffleNode.setInput(0,CreateTree.Lidar1TransformNode)
                CreateTree.Lidar1ShuffleNode.setXYpos(CreateTree.Lidar1TransformNode.xpos(),CreateTree.Lidar1TransformNode.ypos()+40)
                try:
                    if StudioName == "ImageEngine":
                        CreateTree.Lidar1ReadNode["xpos"].setValue(CreateTree.LidarReadNode.xpos()-350)
                        CreateTree.Lidar1ReadNode["ypos"].setValue(CreateTree.LidarReadNode.ypos())
                    else:
                        CreateTree.Lidar1ReadNode["xpos"].setValue(CreateTree.ConesReadNode.xpos()-350)
                        CreateTree.Lidar1ReadNode["ypos"].setValue(CreateTree.ConesReadNode.ypos())
                except:
                    pass
                CreateTree.Lidar1TransformNode.setXYpos(CreateTree.Lidar1ReadNode.xpos(),CreateTree.Lidar1ReadNode.ypos()+100)
                CreateTree.Lidar1ShuffleNode.setXYpos(CreateTree.Lidar1ReadNode.xpos(),CreateTree.Lidar1ReadNode.ypos()+140)
                CreateTree.Lidar1ColorCorrectNode = nuke.createNode('ColorCorrect')
                CreateTree.Lidar1ColorCorrectNode.knob('gamma').setValue(gamma)
                CreateTree.Lidar1ColorCorrectNode.knob('gain').setValue(red,0)    #RED
                CreateTree.Lidar1ColorCorrectNode.knob('gain').setValue(green,1)    #GREEN
                CreateTree.Lidar1ColorCorrectNode.knob('gain').setValue(blue,2)    #BLUE
                CreateTree.Lidar1ColorCorrectNode.knob('gain').setValue(1,3)    #ALPHA
                CreateTree.Lidar1ColorCorrectNode.setXYpos(CreateTree.Lidar1ShuffleNode.xpos(),CreateTree.Lidar1ShuffleNode.ypos()+40)
                CreateTree.Lidar1BlurNode = nuke.createNode('Blur')
                CreateTree.Lidar1BlurNode['disable'].setValue(True)
                CreateTree.Lidar1BlurNode["size"].setValue(1.2,0)
                CreateTree.Lidar1BlurNode.setXYpos(CreateTree.Lidar1ColorCorrectNode.xpos(),CreateTree.Lidar1ColorCorrectNode.ypos()+40)
                CreateTree.Lidar1ErodeNode = nuke.createNode("Dilate")
                CreateTree.Lidar1ErodeNode["size"].setValue(0.5)
                CreateTree.Lidar1ErodeNode['disable'].setValue(True)
                CreateTree.Lidar1ErodeNode.setXYpos(CreateTree.Lidar1BlurNode.xpos(),CreateTree.Lidar1BlurNode.ypos()+40)
                CreateTree.Lidar1MergeNode = nuke.nodes.Merge2()
                CreateTree.Lidar1MergeNode.setInput(1, CreateTree.Lidar1ErodeNode)
                CreateTree.Lidar1MergeNode['label'].setValue(Tree)
                CreateTree.Lidar1MergeNode.setXYpos(CreateTree.Lidar1ErodeNode.xpos(),CreateTree.Lidar1ErodeNode.ypos()+80)
                CreateTree.Lidar1MergeNode['selected'].setValue(False)
                CreateTree.Lidar1MergeNode.knob('mix').setValue(mix)
                for w in nuke.allNodes():
                    w.setSelected(False)
        elif Tree == "Lidar2":
            global Lidar2_Check
            Lidar2_Check = True
            print ("Lidar2_Check = {}".format(Lidar2_Check))   
            for seq in nuke.getFileNameList(Lidar2Path):
                CreateTree.Lidar2ReadNode = nuke.nodes.Read()
                CreateTree.Lidar2ReadNode.knob('file').fromUserText(Lidar2Path + seq)
                CreateTree.Lidar2ReadNode['label'].setValue(Tree)
                CreateTree.Lidar2TransformNode = nuke.createNode("Transform")
                CreateTree.Lidar2TransformNode.setInput(0,CreateTree.Lidar2ReadNode)
                TransformNodes.append(CreateTree.Lidar2TransformNode)
                CreateTree.Lidar2ShuffleNode = nuke.createNode('Shuffle')
                CreateTree.Lidar2ShuffleNode['alpha'].setValue('red')
                CreateTree.Lidar2ShuffleNode.setInput(0,CreateTree.Lidar2TransformNode)
                CreateTree.Lidar2ShuffleNode.setXYpos(CreateTree.Lidar2TransformNode.xpos(),CreateTree.Lidar2TransformNode.ypos()+40)
                try:
                    if StudioName == "ImageEngine":
                        CreateTree.Lidar2ReadNode["xpos"].setValue(CreateTree.Lidar1ReadNode.xpos()-350)
                        CreateTree.Lidar2ReadNode["ypos"].setValue(CreateTree.Lidar1ReadNode.ypos())
                    else:
                        CreateTree.Lidar2ReadNode["xpos"].setValue(CreateTree.ConesReadNode.xpos()-350)
                        CreateTree.Lidar2ReadNode["ypos"].setValue(CreateTree.ConesReadNode.ypos())
                except:
                    pass
                CreateTree.Lidar2TransformNode.setXYpos(CreateTree.Lidar2ReadNode.xpos(),CreateTree.Lidar2ReadNode.ypos()+100)
                CreateTree.Lidar2ShuffleNode.setXYpos(CreateTree.Lidar2ReadNode.xpos(),CreateTree.Lidar2ReadNode.ypos()+140)
                CreateTree.Lidar2ColorCorrectNode = nuke.createNode('ColorCorrect')
                CreateTree.Lidar2ColorCorrectNode.knob('gamma').setValue(gamma)
                CreateTree.Lidar2ColorCorrectNode.knob('gain').setValue(red,0)    #RED
                CreateTree.Lidar2ColorCorrectNode.knob('gain').setValue(green,1)    #GREEN
                CreateTree.Lidar2ColorCorrectNode.knob('gain').setValue(blue,2)    #BLUE
                CreateTree.Lidar2ColorCorrectNode.knob('gain').setValue(1,3)    #ALPHA
                CreateTree.Lidar2ColorCorrectNode.setXYpos(CreateTree.Lidar2ShuffleNode.xpos(),CreateTree.Lidar2ShuffleNode.ypos()+40)
                CreateTree.Lidar2BlurNode = nuke.createNode('Blur')
                CreateTree.Lidar2BlurNode['disable'].setValue(True)
                CreateTree.Lidar2BlurNode["size"].setValue(1.2,0)
                CreateTree.Lidar2BlurNode.setXYpos(CreateTree.Lidar2ColorCorrectNode.xpos(),CreateTree.Lidar2ColorCorrectNode.ypos()+40)
                CreateTree.Lidar2ErodeNode = nuke.createNode("Dilate")
                CreateTree.Lidar2ErodeNode["size"].setValue(0.5)
                CreateTree.Lidar2ErodeNode['disable'].setValue(True)
                CreateTree.Lidar2ErodeNode.setXYpos(CreateTree.Lidar2BlurNode.xpos(),CreateTree.Lidar2BlurNode.ypos()+40)
                CreateTree.Lidar2MergeNode = nuke.nodes.Merge2()
                CreateTree.Lidar2MergeNode.setInput(1, CreateTree.Lidar2ErodeNode)
                CreateTree.Lidar2MergeNode['label'].setValue(Tree)
                CreateTree.Lidar2MergeNode.setXYpos(CreateTree.Lidar2ErodeNode.xpos(),CreateTree.Lidar2ErodeNode.ypos()+80)
                CreateTree.Lidar2MergeNode['selected'].setValue(False)
                CreateTree.Lidar2MergeNode.knob('mix').setValue(mix)
                for w in nuke.allNodes():
                    w.setSelected(False)
        elif Tree == "Rig":
            Rig_Check = True
            print ("Rig_Check = {}".format(Rig_Check)) 
            for seq in nuke.getFileNameList(RigPath):
                CreateTree.RigReadNode = nuke.nodes.Read()
                CreateTree.RigReadNode.knob('file').fromUserText(RigPath + seq)
                CreateTree.RigReadNode['label'].setValue(Tree)
                CreateTree.RigTransformNode = nuke.createNode("Transform")
                CreateTree.RigTransformNode.setInput(0,CreateTree.RigReadNode)
                TransformNodes.append(CreateTree.RigTransformNode)
                CreateTree.RigShuffleNode = nuke.createNode('Shuffle')
                CreateTree.RigShuffleNode['alpha'].setValue('red')
                CreateTree.RigShuffleNode.setInput(0,CreateTree.RigTransformNode)
                CreateTree.RigShuffleNode.setXYpos(CreateTree.RigTransformNode.xpos(),CreateTree.RigTransformNode.ypos()+40)
                try:
                    if Geo_Check == True:
                        CreateTree.RigReadNode["xpos"].setValue(CreateTree.GeoReadNode.xpos()+350)
                        CreateTree.RigReadNode["ypos"].setValue(CreateTree.GeoReadNode.ypos())
                   # elif CreateTree.ConesReadNode and not CreateTree.GeoReadNode:
                    elif Cones_Check == True and Geo_Check == False:
                        if StudioName == "ImageEngine":
                            CreateTree.RigReadNode["xpos"].setValue(CreateTree.ConesReadNode.xpos()+750)
                            CreateTree.RigReadNode["ypos"].setValue(CreateTree.ConesReadNode.ypos())
                        else:
                            CreateTree.RigReadNode["xpos"].setValue(CreateTree.ConesReadNode.xpos()+350)
                            CreateTree.RigReadNode["ypos"].setValue(CreateTree.ConesReadNode.ypos())

                except:
                    pass
                CreateTree.RigTransformNode.setXYpos(CreateTree.RigReadNode.xpos(),CreateTree.RigReadNode.ypos()+100)
                CreateTree.RigShuffleNode.setXYpos(CreateTree.RigReadNode.xpos(),CreateTree.RigReadNode.ypos()+140) 
                CreateTree.RigColorCorrectNode = nuke.createNode('ColorCorrect')
                CreateTree.RigColorCorrectNode.knob('gain').setValue(red,0)    #RED
                CreateTree.RigColorCorrectNode.knob('gain').setValue(green,1)    #GREEN
                CreateTree.RigColorCorrectNode.knob('gain').setValue(blue,2)    #BLUE
                CreateTree.RigColorCorrectNode.knob('gain').setValue(1,3)    #ALPHA
                CreateTree.RigColorCorrectNode.setXYpos(CreateTree.RigShuffleNode.xpos(),CreateTree.RigShuffleNode.ypos()+40)
                CreateTree.RigBlurNode = nuke.createNode('Blur')
                CreateTree.RigBlurNode['disable'].setValue(True)
                CreateTree.RigBlurNode["size"].setValue(1.2,0)
                CreateTree.RigBlurNode.setXYpos(CreateTree.RigColorCorrectNode.xpos(),CreateTree.RigColorCorrectNode.ypos()+40)
                CreateTree.RigErodeNode = nuke.createNode("Dilate")
                CreateTree.RigErodeNode["size"].setValue(0.5)
                CreateTree.RigErodeNode['disable'].setValue(True)
                CreateTree.RigErodeNode.setXYpos(CreateTree.RigBlurNode.xpos(),CreateTree.RigBlurNode.ypos()+40)
                CreateTree.RigMergeNode = nuke.nodes.Merge2()
                CreateTree.RigMergeNode.setInput(1, CreateTree.RigErodeNode)
                CreateTree.RigMergeNode['label'].setValue(Tree)   
                CreateTree.RigMergeNode.setXYpos(CreateTree.RigErodeNode.xpos(),CreateTree.RigErodeNode.ypos()+80)
                CreateTree.RigMergeNode['selected'].setValue(False)
                for w in nuke.allNodes():
                    w.setSelected(False)
##########################################################################################################################################
        elif Tree == "Rig1":
            Rig1_Check = True
            print ("Rig1_Check = {}".format(Rig1_Check)) 
            for seq in nuke.getFileNameList(Rig1Path):
                CreateTree.Rig1ReadNode = nuke.nodes.Read()
                CreateTree.Rig1ReadNode.knob('file').fromUserText(Rig1Path + seq)
                CreateTree.Rig1ReadNode['label'].setValue(Tree)
                CreateTree.Rig1TransformNode = nuke.createNode("Transform")
                CreateTree.Rig1TransformNode.setInput(0,CreateTree.Rig1ReadNode)
                TransformNodes.append(CreateTree.Rig1TransformNode)
                CreateTree.Rig1ShuffleNode = nuke.createNode('Shuffle')
                CreateTree.Rig1ShuffleNode['alpha'].setValue('red')
                CreateTree.Rig1ShuffleNode.setInput(0,CreateTree.Rig1TransformNode)
                CreateTree.Rig1ShuffleNode.setXYpos(CreateTree.Rig1TransformNode.xpos(),CreateTree.Rig1TransformNode.ypos()+40)
                try:
                    if Rig_Check == True:
                        CreateTree.Rig1ReadNode["xpos"].setValue(CreateTree.RigReadNode.xpos()+350)
                        CreateTree.Rig1ReadNode["ypos"].setValue(CreateTree.RigReadNode.ypos())
                except:
                    pass
                CreateTree.Rig1TransformNode.setXYpos(CreateTree.Rig1ReadNode.xpos(),CreateTree.Rig1ReadNode.ypos()+100)
                CreateTree.Rig1ShuffleNode.setXYpos(CreateTree.Rig1ReadNode.xpos(),CreateTree.Rig1ReadNode.ypos()+140) 
                CreateTree.Rig1ColorCorrectNode = nuke.createNode('ColorCorrect')
                CreateTree.Rig1ColorCorrectNode.knob('gain').setValue(red,0)    #RED
                CreateTree.Rig1ColorCorrectNode.knob('gain').setValue(green,1)    #GREEN
                CreateTree.Rig1ColorCorrectNode.knob('gain').setValue(blue,2)    #BLUE
                CreateTree.Rig1ColorCorrectNode.knob('gain').setValue(1,3)    #ALPHA
                CreateTree.Rig1ColorCorrectNode.setXYpos(CreateTree.Rig1ShuffleNode.xpos(),CreateTree.Rig1ShuffleNode.ypos()+40)
                CreateTree.Rig1BlurNode = nuke.createNode('Blur')
                CreateTree.Rig1BlurNode['disable'].setValue(True)
                CreateTree.Rig1BlurNode["size"].setValue(1.2,0)
                CreateTree.Rig1BlurNode.setXYpos(CreateTree.Rig1ColorCorrectNode.xpos(),CreateTree.Rig1ColorCorrectNode.ypos()+40)
                CreateTree.Rig1ErodeNode = nuke.createNode("Dilate")
                CreateTree.Rig1ErodeNode["size"].setValue(0.5)
                CreateTree.Rig1ErodeNode['disable'].setValue(True)
                CreateTree.Rig1ErodeNode.setXYpos(CreateTree.Rig1BlurNode.xpos(),CreateTree.Rig1BlurNode.ypos()+40)
                CreateTree.Rig1MergeNode = nuke.createNode('Merge2')
                CreateTree.Rig1MergeNode['label'].setValue(Tree)   
                CreateTree.Rig1MergeNode.setXYpos(CreateTree.Rig1ErodeNode.xpos(),CreateTree.Rig1ErodeNode.ypos()+80)
                CreateTree.Rig1MergeNode['selected'].setValue(False)
        elif Tree == "Rig2":
            Rig2_Check = True
            print ("Rig2_Check = {}".format(Rig2_Check)) 
            for seq in nuke.getFileNameList(Rig2Path):
                CreateTree.Rig2ReadNode = nuke.nodes.Read()
                CreateTree.Rig2ReadNode.knob('file').fromUserText(Rig2Path + seq)
                CreateTree.Rig2ReadNode['label'].setValue(Tree)
                CreateTree.Rig2TransformNode = nuke.createNode("Transform")
                CreateTree.Rig2TransformNode.setInput(0,CreateTree.Rig2ReadNode)  
                TransformNodes.append(CreateTree.Rig2TransformNode)
                CreateTree.Rig2ShuffleNode = nuke.createNode('Shuffle')
                CreateTree.Rig2ShuffleNode['alpha'].setValue('red')
                CreateTree.Rig2ShuffleNode.setInput(0,CreateTree.Rig2TransformNode)
                CreateTree.Rig2ShuffleNode.setXYpos(CreateTree.Rig2TransformNode.xpos(),CreateTree.Rig2TransformNode.ypos()+40)
                try:
                    if Rig1_Check == True:
                        CreateTree.Rig2ReadNode["xpos"].setValue(CreateTree.Rig1ReadNode.xpos()+350)
                        CreateTree.Rig2ReadNode["ypos"].setValue(CreateTree.Rig1ReadNode.ypos())
                except:
                    pass
                CreateTree.Rig2TransformNode.setXYpos(CreateTree.Rig2ReadNode.xpos(),CreateTree.Rig2ReadNode.ypos()+100)
                CreateTree.Rig2ShuffleNode.setXYpos(CreateTree.Rig2ReadNode.xpos(),CreateTree.Rig2ReadNode.ypos()+140) 
                CreateTree.Rig2ColorCorrectNode = nuke.createNode('ColorCorrect')
                CreateTree.Rig2ColorCorrectNode.knob('gain').setValue(red,0)    #RED
                CreateTree.Rig2ColorCorrectNode.knob('gain').setValue(green,1)    #GREEN
                CreateTree.Rig2ColorCorrectNode.knob('gain').setValue(blue,2)    #BLUE
                CreateTree.Rig2ColorCorrectNode.knob('gain').setValue(1,3)    #ALPHA
                CreateTree.Rig2ColorCorrectNode.setXYpos(CreateTree.Rig2ShuffleNode.xpos(),CreateTree.Rig2ShuffleNode.ypos()+40)
                CreateTree.Rig2BlurNode = nuke.createNode('Blur')
                CreateTree.Rig2BlurNode['disable'].setValue(True)
                CreateTree.Rig2BlurNode["size"].setValue(1.2,0)
                CreateTree.Rig2BlurNode.setXYpos(CreateTree.Rig2ColorCorrectNode.xpos(),CreateTree.Rig2ColorCorrectNode.ypos()+40)
                CreateTree.Rig2ErodeNode = nuke.createNode("Dilate")
                CreateTree.Rig2ErodeNode["size"].setValue(0.5)
                CreateTree.Rig2ErodeNode['disable'].setValue(True)
                CreateTree.Rig2ErodeNode.setXYpos(CreateTree.Rig2BlurNode.xpos(),CreateTree.Rig2BlurNode.ypos()+40)
                CreateTree.Rig2MergeNode = nuke.createNode('Merge2')
                CreateTree.Rig2MergeNode['label'].setValue(Tree)   
                CreateTree.Rig2MergeNode.setXYpos(CreateTree.Rig2ErodeNode.xpos(),CreateTree.Rig2ErodeNode.ypos()+80)
                CreateTree.Rig2MergeNode['selected'].setValue(False)
        elif Tree == "Rig3":
            Rig3_Check = True
            print ("Rig3_Check = {}".format(Rig3_Check)) 
            for seq in nuke.getFileNameList(Rig3Path):
                CreateTree.Rig3ReadNode = nuke.nodes.Read()
                CreateTree.Rig3ReadNode.knob('file').fromUserText(Rig3Path + seq)
                CreateTree.Rig3ReadNode['label'].setValue(Tree)
                CreateTree.Rig3TransformNode = nuke.createNode("Transform")
                CreateTree.Rig3TransformNode.setInput(0,CreateTree.Rig3ReadNode) 
                TransformNodes.append(CreateTree.Rig3TransformNode)
                CreateTree.Rig3ShuffleNode = nuke.createNode('Shuffle')
                CreateTree.Rig3ShuffleNode['alpha'].setValue('red')
                CreateTree.Rig3ShuffleNode.setInput(0,CreateTree.Rig3TransformNode)
                CreateTree.Rig3ShuffleNode.setXYpos(CreateTree.Rig3TransformNode.xpos(),CreateTree.Rig3TransformNode.ypos()+40)
                try:
                    if Rig2_Check == True:
                        CreateTree.Rig3ReadNode["xpos"].setValue(CreateTree.Rig2ReadNode.xpos()+350)
                        CreateTree.Rig3ReadNode["ypos"].setValue(CreateTree.Rig2ReadNode.ypos())
                except:
                    pass
                CreateTree.Rig3TransformNode.setXYpos(CreateTree.Rig3ReadNode.xpos(),CreateTree.Rig3ReadNode.ypos()+100)
                CreateTree.Rig3ShuffleNode.setXYpos(CreateTree.Rig3ReadNode.xpos(),CreateTree.Rig3ReadNode.ypos()+140) 
                CreateTree.Rig3ColorCorrectNode = nuke.createNode('ColorCorrect')
                CreateTree.Rig3ColorCorrectNode.knob('gain').setValue(red,0)    #RED
                CreateTree.Rig3ColorCorrectNode.knob('gain').setValue(green,1)    #GREEN
                CreateTree.Rig3ColorCorrectNode.knob('gain').setValue(blue,2)    #BLUE
                CreateTree.Rig3ColorCorrectNode.knob('gain').setValue(1,3)    #ALPHA
                CreateTree.Rig3ColorCorrectNode.setXYpos(CreateTree.Rig3ShuffleNode.xpos(),CreateTree.Rig3ShuffleNode.ypos()+40)
                CreateTree.Rig3BlurNode = nuke.createNode('Blur')
                CreateTree.Rig3BlurNode['disable'].setValue(True)
                CreateTree.Rig3BlurNode["size"].setValue(1.2,0)
                CreateTree.Rig3BlurNode.setXYpos(CreateTree.Rig3ColorCorrectNode.xpos(),CreateTree.Rig3ColorCorrectNode.ypos()+40)
                CreateTree.Rig3ErodeNode = nuke.createNode("Dilate")
                CreateTree.Rig3ErodeNode["size"].setValue(0.5)
                CreateTree.Rig3ErodeNode['disable'].setValue(True)
                CreateTree.Rig3ErodeNode.setXYpos(CreateTree.Rig3BlurNode.xpos(),CreateTree.Rig3BlurNode.ypos()+40)
                CreateTree.Rig3MergeNode = nuke.createNode('Merge2')
                CreateTree.Rig3MergeNode['label'].setValue(Tree)   
                CreateTree.Rig3MergeNode.setXYpos(CreateTree.Rig3ErodeNode.xpos(),CreateTree.Rig3ErodeNode.ypos()+80)
                CreateTree.Rig3MergeNode['selected'].setValue(False)
        elif Tree == "Rig4":
            Rig4_Check = True
            print ("Rig4_Check = {}".format(Rig4_Check)) 
            for seq in nuke.getFileNameList(Rig4Path):
                CreateTree.Rig4ReadNode = nuke.nodes.Read()
                CreateTree.Rig4ReadNode.knob('file').fromUserText(Rig4Path + seq)
                CreateTree.Rig4ReadNode['label'].setValue(Tree)
                CreateTree.Rig4TransformNode = nuke.createNode("Transform")
                CreateTree.Rig4TransformNode.setInput(0,CreateTree.Rig4ReadNode)
                TransformNodes.append(CreateTree.Rig4TransformNode)
                CreateTree.Rig4ShuffleNode = nuke.createNode('Shuffle')
                CreateTree.Rig4ShuffleNode['alpha'].setValue('red')
                CreateTree.Rig4ShuffleNode.setInput(0,CreateTree.Rig4TransformNode)
                CreateTree.Rig4ShuffleNode.setXYpos(CreateTree.Rig4TransformNode.xpos(),CreateTree.Rig4TransformNode.ypos()+40)
                try:
                    if Rig3_Check == True:
                        CreateTree.Rig4ReadNode["xpos"].setValue(CreateTree.Rig3ReadNode.xpos()+350)
                        CreateTree.Rig4ReadNode["ypos"].setValue(CreateTree.Rig3ReadNode.ypos())
                except:
                    pass
                CreateTree.Rig4TransformNode.setXYpos(CreateTree.Rig4ReadNode.xpos(),CreateTree.Rig4ReadNode.ypos()+100)
                CreateTree.Rig4ShuffleNode.setXYpos(CreateTree.Rig4ReadNode.xpos(),CreateTree.Rig4ReadNode.ypos()+140) 
                CreateTree.Rig4ColorCorrectNode = nuke.createNode('ColorCorrect')
                CreateTree.Rig4ColorCorrectNode.knob('gain').setValue(red,0)    #RED
                CreateTree.Rig4ColorCorrectNode.knob('gain').setValue(green,1)    #GREEN
                CreateTree.Rig4ColorCorrectNode.knob('gain').setValue(blue,2)    #BLUE
                CreateTree.Rig4ColorCorrectNode.knob('gain').setValue(1,3)    #ALPHA
                CreateTree.Rig4ColorCorrectNode.setXYpos(CreateTree.Rig4ShuffleNode.xpos(),CreateTree.Rig4ShuffleNode.ypos()+40)
                CreateTree.Rig4BlurNode = nuke.createNode('Blur')
                CreateTree.Rig4BlurNode['disable'].setValue(True)
                CreateTree.Rig4BlurNode["size"].setValue(1.2,0)
                CreateTree.Rig4BlurNode.setXYpos(CreateTree.Rig4ColorCorrectNode.xpos(),CreateTree.Rig4ColorCorrectNode.ypos()+40)
                CreateTree.Rig4ErodeNode = nuke.createNode("Dilate")
                CreateTree.Rig4ErodeNode["size"].setValue(0.5)
                CreateTree.Rig4ErodeNode['disable'].setValue(True)
                CreateTree.Rig4ErodeNode.setXYpos(CreateTree.Rig4BlurNode.xpos(),CreateTree.Rig4BlurNode.ypos()+40)
                CreateTree.Rig4MergeNode = nuke.createNode('Merge2')
                CreateTree.Rig4MergeNode['label'].setValue(Tree)   
                CreateTree.Rig4MergeNode.setXYpos(CreateTree.Rig4ErodeNode.xpos(),CreateTree.Rig4ErodeNode.ypos()+80)
                CreateTree.Rig4MergeNode['selected'].setValue(False)
        elif Tree == "Rig5":
            Rig5_Check = True
            print ("Rig5_Check = {}".format(Rig5_Check)) 
            for seq in nuke.getFileNameList(Rig5Path):
                CreateTree.Rig5ReadNode = nuke.nodes.Read()
                CreateTree.Rig5ReadNode.knob('file').fromUserText(Rig5Path + seq)
                CreateTree.Rig5ReadNode['label'].setValue(Tree)
                CreateTree.Rig5TransformNode = nuke.createNode("Transform")
                CreateTree.Rig5TransformNode.setInput(0,CreateTree.Rig5ReadNode) 
                TransformNodes.append(CreateTree.Rig5TransformNode)
                CreateTree.Rig5ShuffleNode = nuke.createNode('Shuffle')
                CreateTree.Rig5ShuffleNode['alpha'].setValue('red')
                CreateTree.Rig5ShuffleNode.setInput(0,CreateTree.Rig5TransformNode)
                CreateTree.Rig5ShuffleNode.setXYpos(CreateTree.Rig5TransformNode.xpos(),CreateTree.Rig5TransformNode.ypos()+40)
                try:
                    if Rig4_Check == True:
                        CreateTree.Rig5ReadNode["xpos"].setValue(CreateTree.Rig4ReadNode.xpos()+350)
                        CreateTree.Rig5ReadNode["ypos"].setValue(CreateTree.Rig4ReadNode.ypos())
                except:
                    pass
                CreateTree.Rig5TransformNode.setXYpos(CreateTree.Rig5ReadNode.xpos(),CreateTree.Rig5ReadNode.ypos()+100)
                CreateTree.Rig5ShuffleNode.setXYpos(CreateTree.Rig5ReadNode.xpos(),CreateTree.Rig5ReadNode.ypos()+140) 
                CreateTree.Rig5ColorCorrectNode = nuke.createNode('ColorCorrect')
                CreateTree.Rig5ColorCorrectNode.knob('gain').setValue(red,0)    #RED
                CreateTree.Rig5ColorCorrectNode.knob('gain').setValue(green,1)    #GREEN
                CreateTree.Rig5ColorCorrectNode.knob('gain').setValue(blue,2)    #BLUE
                CreateTree.Rig5ColorCorrectNode.knob('gain').setValue(1,3)    #ALPHA
                CreateTree.Rig5ColorCorrectNode.setXYpos(CreateTree.Rig5ShuffleNode.xpos(),CreateTree.Rig5ShuffleNode.ypos()+40)
                CreateTree.Rig5BlurNode = nuke.createNode('Blur')
                CreateTree.Rig5BlurNode['disable'].setValue(True)
                CreateTree.Rig5BlurNode["size"].setValue(1.2,0)
                CreateTree.Rig5BlurNode.setXYpos(CreateTree.Rig5ColorCorrectNode.xpos(),CreateTree.Rig5ColorCorrectNode.ypos()+40)
                CreateTree.Rig5ErodeNode = nuke.createNode("Dilate")
                CreateTree.Rig5ErodeNode["size"].setValue(0.5)
                CreateTree.Rig5ErodeNode['disable'].setValue(True)
                CreateTree.Rig5ErodeNode.setXYpos(CreateTree.Rig5BlurNode.xpos(),CreateTree.Rig5BlurNode.ypos()+40)
                CreateTree.Rig5MergeNode = nuke.createNode('Merge2')
                CreateTree.Rig5MergeNode['label'].setValue(Tree)   
                CreateTree.Rig5MergeNode.setXYpos(CreateTree.Rig5ErodeNode.xpos(),CreateTree.Rig5ErodeNode.ypos()+80)
                CreateTree.Rig5MergeNode['selected'].setValue(False)
    if os.path.exists(Main3dPath):
        for folders in nuke.getFileNameList(Main3dPath):
            if folders == "CONES":
                if len(os.listdir(ConesPath))>0:
                    if StudioName == "Framestore":
                        CreateTree(Tree="Cones",red=1,green=0,blue=0,mix=1,gamma=1.0)           # Red Cones
                    else:
                        CreateTree(Tree="Cones",red=1,green=0,blue=1,mix=1,gamma=1.0)           # Pink Cones
                else:
                    nuke.message("Missing Cone Renders")
                    
            elif folders == "GEO":

    #            print ("ListOfGeoSUM = {}".format(ListOfGeoSUM))    
    #            print ("ListOfGeoAverage = {}".format(ListOfGeoAverage)) 
            #   if StudioName == "ImageEngine":
            #       CreateTree(Tree="Lidar",red=1,green=1,blue=0,mix=0.4,gamma=1.0)
                    
                if len(os.listdir(GeoPath))>0:
                    ListOfGeo=[]
                    for file in os.listdir(GeoPath):
                        size = os.stat(GeoPath + file).st_size
                        Megabyte = size/1000000.0
                        ListOfGeo.append(Megabyte)

                    ListOfGeoSUM = sum(ListOfGeo)
                    ListOfGeoAverage = ListOfGeoSUM / len(ListOfGeo)
                    if ListOfGeoAverage > 3.0:
                        CreateTree(Tree="Geo",red=1,green=1,blue=0,mix=0.2,gamma=1.0)
                    elif ListOfGeoAverage < 3.0:
                        CreateTree(Tree="Geo",red=1,green=1,blue=0,mix=0.2,gamma=1.0)
                else:
                    nuke.message("Missing Geo Renders")
                    
            #    else:
                
            elif folders == "LIDAR":
                if len(os.listdir(GeoPath))>0:
                    if StudioName == "ImageEngine":
                        Geo_Check = True
                        CreateTree(Tree="Lidar",red=1,green=1,blue=0,mix=0.2,gamma=1.0)
                else:
                    nuke.message("Missing Lidar Renders")

            elif folders == "LIDAR1":
                if len(os.listdir(GeoPath))>0:
                    if StudioName == "ImageEngine":
                        Geo_Check = True
                        CreateTree(Tree="Lidar1",red=0.0,green=0.23,blue=0.6,mix=0.83,gamma=1.0)
                else:
                    nuke.message("Missing Lidar Renders")            
                    
            elif folders == "LIDAR2":
                if len(os.listdir(GeoPath))>0:
                    if StudioName == "ImageEngine":
                        Geo_Check = True
                        CreateTree(Tree="Lidar2",red=0.83,green=0.57,blue=0.19,mix=0.2,gamma=1.0)
                else:
                    nuke.message("Missing Lidar Renders")                   
                    
                
            #    else:
            #        CreateTree(Tree="Rig",red=0,green=1,blue=1,mix=1,gamma=1.0)


            elif folders == "RIG":
                if len(os.listdir(RigPath))>0:
                    if StudioName == "ImageEngine":
                        if Geo_Check:
                            CreateTree(Tree="Geo",red=1,green=1,blue=0,mix=1.0,gamma=1.0)
                        CreateTree(Tree="Rig",red=0,green=1,blue=1,mix=1,gamma=1.0)
                    else:
                        CreateTree(Tree="Rig",red=0,green=1,blue=1,mix=1,gamma=1.0)
                else:
                    nuke.message("Missing Rig Renders")   


            elif folders == "RIG1":
                if len(os.listdir(Rig1Path))>0:
                    CreateTree(Tree="Rig1",red=0.04,green=0.33,blue=1.82,mix=1,gamma=1.0)       #Rig 1 Color = 173342719
                else:
                    nuke.message("Missing Rig1 Renders")
            elif folders == "RIG2":
                if len(os.listdir(Rig2Path))>0:
                    CreateTree(Tree="Rig2",red=0.1,green=1.82,blue=0.08,mix=1,gamma=1.0)        #Rig 2 Color = 436147455
                else:
                    nuke.message("Missing Rig2 Renders")
            elif folders == "RIG3":
                if len(os.listdir(Rig3Path))>0:
                    CreateTree(Tree="Rig3",red=2.7,green=0.29,blue=0.31,mix=1,gamma=1.0)        #Rig 3 Color = 4282993919
                else:
                    nuke.message("Missing Rig3 Renders")
            elif folders == "RIG4":
                if len(os.listdir(Rig4Path))>0:
                    CreateTree(Tree="Rig4",red=1.82,green=0,blue=0.10,mix=1,gamma=1.0)          #Rig 4 Color = 4278196735
                else:
                    nuke.message("Missing Rig4 Renders")   
            elif folders == "RIG5":
                if len(os.listdir(Rig5Path))>0:
                    CreateTree(Tree="Rig5",red=1.82,green=0.4573,blue=0.11,mix=1,gamma=1.0)     #Rig 5 Color = 4285799679
                else:
                    nuke.message("Missing Rig5 Renders")

    else:
        All_Versions = []
        _Expected_Version = render_Path + "/main3d/"
        for ev in os.listdir(_Expected_Version):
            if "v0" in ev:
                All_Versions.append(ev)
        print("All_Versions: {}".format(All_Versions))

        Expected_Version = str(All_Versions[-1])
        Xpected=Expected_Version
        nuke.message("""Version mismatch, latest maya version must be equal to rendered version
                    Maya Version = {}, expected Render Version ={}
                    Render Version Loaded = {}
                    """.format(Version,Expected_Version,Expected_Version))  
        
        Main3dPath_Altered = render_Path + "/main3d/" + Xpected + "/"
        Main3dPath_Altered = Main3dPath_Altered.replace("\\","/")
        print("Expected_Version: {}".format(Expected_Version))
        print("Main3dPath_Altered: {}".format(Main3dPath_Altered))

        ConesPath=Main3dPath_Altered + "CONES/"
        ConesPath=ConesPath.replace("\\","/")
        GeoPath=Main3dPath_Altered + "GEO/"
        GeoPath=GeoPath.replace("\\","/")
        RigPath=Main3dPath_Altered + "RIG/"
        RigPath=RigPath.replace("\\","/")
        Rig1Path=Main3dPath_Altered + "RIG1/"
        Rig1Path=Rig1Path.replace("\\","/")
        Rig2Path=Main3dPath_Altered + "RIG2/"
        Rig2Path=Rig2Path.replace("\\","/")
        Rig3Path=Main3dPath_Altered + "RIG3/"
        Rig3Path=Rig3Path.replace("\\","/")
        Rig4Path=Main3dPath_Altered + "RIG4/"
        Rig4Path=Rig4Path.replace("\\","/")
        Rig5Path=Main3dPath_Altered + "RIG5/"
        Rig5Path=Rig5Path.replace("\\","/")
        
           
        for folders in nuke.getFileNameList(Main3dPath_Altered):
            if folders == "CONES":
                if len(os.listdir(ConesPath))>0:
                    if StudioName == "Framestore":
                        CreateTree(Tree="Cones",red=1,green=0,blue=0,mix=1,gamma=1.0)           # Red Cones
                    else:
                        CreateTree(Tree="Cones",red=1,green=0,blue=1,mix=1,gamma=1.0)           # Pink Cones
                else:
                    nuke.message("Missing Cone Renders")
                    
            elif folders == "GEO":

    #            print ("ListOfGeoSUM = {}".format(ListOfGeoSUM))    
    #            print ("ListOfGeoAverage = {}".format(ListOfGeoAverage)) 
            #   if StudioName == "ImageEngine":
            #       CreateTree(Tree="Lidar",red=1,green=1,blue=0,mix=0.4,gamma=1.0)
                    
                if len(os.listdir(GeoPath))>0:
                    ListOfGeo=[]
                    for file in os.listdir(GeoPath):
                        size = os.stat(GeoPath + file).st_size
                        Megabyte = size/1000000.0
                        ListOfGeo.append(Megabyte)

                    ListOfGeoSUM = sum(ListOfGeo)
                    ListOfGeoAverage = ListOfGeoSUM / len(ListOfGeo)
                    if ListOfGeoAverage > 3.0:
                        CreateTree(Tree="Geo",red=1,green=1,blue=0,mix=0.2,gamma=1.0)
                    elif ListOfGeoAverage < 3.0:
                        CreateTree(Tree="Geo",red=1,green=1,blue=0,mix=0.2,gamma=1.0)
                else:
                    nuke.message("Missing Geo Renders")
                    
            #    else:
                
            elif folders == "LIDAR":
                if len(os.listdir(GeoPath))>0:
                    if StudioName == "ImageEngine":
                        Geo_Check = True
                        CreateTree(Tree="Lidar",red=1,green=1,blue=0,mix=0.2,gamma=1.0)
                else:
                    nuke.message("Missing Lidar Renders")

            elif folders == "LIDAR1":
                if len(os.listdir(GeoPath))>0:
                    if StudioName == "ImageEngine":
                        Geo_Check = True
                        CreateTree(Tree="Lidar1",red=0.0,green=0.23,blue=0.6,mix=0.83,gamma=1.0)
                else:
                    nuke.message("Missing Lidar Renders")            
                    
            elif folders == "LIDAR2":
                if len(os.listdir(GeoPath))>0:
                    if StudioName == "ImageEngine":
                        Geo_Check = True
                        CreateTree(Tree="Lidar2",red=0.83,green=0.57,blue=0.19,mix=0.2,gamma=1.0)
                else:
                    nuke.message("Missing Lidar Renders")                   
                    
                
            #    else:
            #        CreateTree(Tree="Rig",red=0,green=1,blue=1,mix=1,gamma=1.0)


            elif folders == "RIG":
                if len(os.listdir(RigPath))>0:
                    if StudioName == "ImageEngine":
                        if Geo_Check:
                            CreateTree(Tree="Geo",red=1,green=1,blue=0,mix=1.0,gamma=1.0)
                        CreateTree(Tree="Rig",red=0,green=1,blue=1,mix=1,gamma=1.0)
                    else:
                        CreateTree(Tree="Rig",red=0,green=1,blue=1,mix=1,gamma=1.0)
                else:
                    nuke.message("Missing Rig Renders")   


            elif folders == "RIG1":
                if len(os.listdir(Rig1Path))>0:
                    CreateTree(Tree="Rig1",red=0.04,green=0.33,blue=1.82,mix=1,gamma=1.0)       #Rig 1 Color = 173342719
                else:
                    nuke.message("Missing Rig1 Renders")
            elif folders == "RIG2":
                if len(os.listdir(Rig2Path))>0:
                    CreateTree(Tree="Rig2",red=0.1,green=1.82,blue=0.08,mix=1,gamma=1.0)        #Rig 2 Color = 436147455
                else:
                    nuke.message("Missing Rig2 Renders")
            elif folders == "RIG3":
                if len(os.listdir(Rig3Path))>0:
                    CreateTree(Tree="Rig3",red=2.7,green=0.29,blue=0.31,mix=1,gamma=1.0)        #Rig 3 Color = 4282993919
                else:
                    nuke.message("Missing Rig3 Renders")
            elif folders == "RIG4":
                if len(os.listdir(Rig4Path))>0:
                    CreateTree(Tree="Rig4",red=1.82,green=0,blue=0.10,mix=1,gamma=1.0)          #Rig 4 Color = 4278196735
                else:
                    nuke.message("Missing Rig4 Renders")   
            elif folders == "RIG5":
                if len(os.listdir(Rig5Path))>0:
                    CreateTree(Tree="Rig5",red=1.82,green=0.4573,blue=0.11,mix=1,gamma=1.0)     #Rig 5 Color = 4285799679
                else:
                    nuke.message("Missing Rig5 Renders")   


    #####
    #       Connecting the Merge nodes from all Trees
    #####
    if Cones_Check == True and Geo_Check == True and Rig_Check == True:    
        try:
            if CreateTree.GeoMergeNode and CreateTree.RigMergeNode and CreateTree.ConesMergeNode:
                if StudioName == "ImageEngine":
                    CreateTree.GeoMergeNode.setInput(0,CreateTree.RigMergeNode)
                
                else:
                    CreateTree.GeoMergeNode.setInput(0,CreateTree.RigMergeNode)
                    CreateTree.ConesMergeNode.setInput(0,CreateTree.GeoMergeNode)
                    print ("All 3")
        except:
            pass
    elif Cones_Check == True and Geo_Check == True:
        try:
            if CreateTree.ConesMergeNode and CreateTree.GeoMergeNode:
                if StudioName == "ImageEngine":
                    pass
                else:
                    CreateTree.ConesMergeNode.setInput(0,CreateTree.GeoMergeNode)
                    print ("Cones and Geo")
        except:
            pass
    elif Cones_Check == True and Rig_Check == True:
        try:
            if CreateTree.ConesMergeNode and CreateTree.RigMergeNode:
                if StudioName == "ImageEngine":
                    pass
                else:
                    CreateTree.ConesMergeNode.setInput(0,CreateTree.RigMergeNode)
                    print ("Cones and Rig")
        except:
            pass
    elif Cones_Check == False and Geo_Check == True and Rig_Check == True:
        try:
            if CreateTree.GeoMergeNode and CreateTree.RigMergeNode:
                CreateTree.GeoMergeNode.setInput(0,CreateTree.RigMergeNode)
                print ("Geo and Rig")
        except:
            pass
    elif Cones_Check == False and Geo_Check == False and Rig_Check == False:
        try:
            nuke.message("Missing CONES/GEO/RIG  BE BRAT!")
        except:
            pass
### Lidar Connection
    try:
        if CreateTree.LidarMergeNode and CreateTree.Lidar1MergeNode:
            CreateTree.LidarMergeNode.setInput(0,CreateTree.Lidar1MergeNode)
    except:
        pass
    try:
        if CreateTree.Lidar1MergeNode and CreateTree.Lidar2MergeNode:
            CreateTree.Lidar1MergeNode.setInput(0,CreateTree.Lidar2MergeNode)
    except:
        pass

####
    try:
        if CreateTree.RigMergeNode and CreateTree.Rig1MergeNode:
            CreateTree.RigMergeNode.setInput(0,CreateTree.Rig1MergeNode)
    except:
        pass
    try:
        if CreateTree.Rig1MergeNode and CreateTree.Rig2MergeNode:
            CreateTree.Rig1MergeNode.setInput(0,CreateTree.Rig2MergeNode)
    except:
        pass
    try:
        if CreateTree.Rig2MergeNode and CreateTree.Rig3MergeNode:
            CreateTree.Rig2MergeNode.setInput(0,CreateTree.Rig3MergeNode)
    except:
        pass
    try:
        if CreateTree.Rig3MergeNode and CreateTree.Rig4MergeNode:
            CreateTree.Rig3MergeNode.setInput(0,CreateTree.Rig4MergeNode)
    except:
        pass
    try:
        if CreateTree.Rig4MergeNode and CreateTree.Rig5MergeNode:
            CreateTree.Rig4MergeNode.setInput(0,CreateTree.Rig5MergeNode)
    except:
        pass
####
    


    MergeTreesNode = nuke.nodes.Merge2()
#    print ("Cones_Check = {}".format(Cones_Check)) 
#    print ("Geo_Check = {}".format(Geo_Check)) 
#    print ("Rig_Check = {}".format(Rig_Check)) 
    if StudioName != "ImageEngine":
        if Cones_Check == True:
            MergeTreesNode.setInput(1,CreateTree.ConesMergeNode)
            MergeTreesNode.setXYpos(CreateTree.ConesMergeNode.xpos(),CreateTree.ConesMergeNode.ypos()+100)
            MergeTreesNode['label'].setValue("ALL")
            BlurAllNode = nuke.createNode("Blur")
            BlurAllNode.setXYpos(MergeTreesNode.xpos(),MergeTreesNode.ypos()+80)
            BlurAllNode.setInput(0,MergeTreesNode)
            BlurAllNode["size"].setValue(1.2)
            # IF this is an LD node type of shot
            if LDCheck == True and UV_LD_Status == "LD Node" :
                try:
                    for seq in nuke.getFileNameList(JPGPath):
                        Split = seq.split(" ")
                        Split.pop()
                        Split = "".join(Split)
                        if Split.endswith(".jpg"):
                            Read_JPG = nuke.createNode('Read')
                            Read_JPG.knob('file').fromUserText(JPGPath + seq)
                            JpgFirstFrame = Read_JPG['first'].value()
                            JpgLastFrame = Read_JPG['last'].value()
                            JPG_FORMAT = Read_JPG['format'].value()
                            PixelAspectJPG = Read_JPG.pixelAspect()
                            ReformatLDNode = nuke.nodes.Reformat()
                            ReformatLDNode['format'].setValue(JPG_FORMAT)
                            ReformatLDNode['black_outside'].setValue(True)
                            ReformatLDNode['pbb'].setValue(True)
                            ReformatLDNode['resize'].setValue("none")
                            ReformatLDNode.setXYpos(BlurAllNode.xpos(),BlurAllNode.ypos()+80)
                            ReformatLDNode.setInput(0,BlurAllNode)
                            
                except:
                    nuke.message('Cannot find JPG')
                    pass

                for LD in os.listdir(LDNodePath):
                    if "dist_".lower() in LD.lower():
                        Split,ext = os.path.splitext(LD)
                        SplitDist = Split.split("_")
                        for v in SplitDist:
                            if "v0" in v:
                                LastVersion = v
                                
                    try:
                        LastVersion
                    except NameError:
                        pass
                for LD in os.listdir(LDNodePath):
                    try:
                        if "dist_{}".format(LastVersion).lower() in LD.lower():
                            LDNodePath = LDNodePath + LD
                            LDNode = nuke.nodePaste(LDNodePath)
                            LDNode['direction'].setValue("distort")
                            LDNode['name'].setValue(LDNode.name() + "_" + LastVersion)
                            LDNode.setInput(0,ReformatLDNode)
                            LDNode.setXYpos(ReformatLDNode.xpos(),ReformatLDNode.ypos()+80)
                            MergeFinalNode = nuke.nodes.Merge2()
                            MergeFinalNode.setXYpos(LDNode.xpos(),LDNode.ypos()+120)
                            MergeFinalNode.setInput(1,LDNode)
                            MergeFinalNode["name"].setValue("Merge")
                            MergeFinalNode["label"].setValue("FINAL")
                            MergeFinalNode.setInput(0,Read_JPG)
                            Read_JPG.setXYpos(MergeFinalNode.xpos()+300,MergeFinalNode.ypos()-25)
                    except:
                            pass
                CONES_FORMAT = CreateTree.ConesReadNode['format'].actualValue()
                CONES_WIDTH = CONES_FORMAT.width()
                CONES_HEIGHT = CONES_FORMAT.height()
                JPG_HEIGHT = JPG_FORMAT.height()
                JPG_WIDTH = JPG_FORMAT.width()

                Image_Aspect = JPG_WIDTH / JPG_HEIGHT
                if Image_Aspect > 2.0:
                    Anamorphic = True

                print ("Anamorphic = {}".format(Anamorphic))
                print ("CONES_FORMAT = {}".format(CONES_FORMAT))
                print ("CONES_WIDTH = {}".format(CONES_WIDTH))
                print ("CONES_HEIGHT = {}".format(CONES_HEIGHT))
                print ("JPG_HEIGHT = {}".format(JPG_HEIGHT))
                print ("JPG_WIDTH = {}".format(JPG_WIDTH))
                
            #IF it is a UV MAP type of shot
            else:
                for uv in nuke.getFileNameList(UVDistortPath):
                    print (uv)
                    try:
                        if "redi" in uv.lower():
                            Read_RedistortEXR = nuke.createNode('Read')
                            Read_RedistortEXR.knob('file').fromUserText(UVDistortPath + uv)
            
                    except:
                        nuke.message("Missing Redist Map, name it 'redist' ")
                        pass

                STMapNode = nuke.nodes.STMap (uv="rgba")
                STMapNode.setInput(0,BlurAllNode)
                #    STMapNode.setInput(1,RedistNode)
                STMapNode.setXYpos(BlurAllNode.xpos(),BlurAllNode.ypos()+80)
                try:
                    STMapNode.setInput(1,Read_RedistortEXR)
                except:
                    pass
                try:
                    Read_RedistortEXR.setXYpos(STMapNode.xpos()+150,STMapNode.ypos()-25)
                except:
                    pass
                MergeFinalNode = nuke.nodes.Merge2()
                MergeFinalNode.setXYpos(STMapNode.xpos(),STMapNode.ypos()+120)
        #        MergeFinalNode.setInput(0,STMapNode)
                MergeFinalNode.setInput(1,STMapNode)
                MergeFinalNode["name"].setValue("Merge")
                MergeFinalNode["label"].setValue("FINAL")

                try:
                    for seq in nuke.getFileNameList(JPGPath):
                        Split = seq.split(" ")
                        Split.pop()
                        Split = "".join(Split)
                        if Split.endswith(".jpg"):
                            Read_JPG = nuke.createNode('Read')
                            try:
                                Read_JPG.knob('file').fromUserText(JPGPath + seq)
                                Read_JPG.setXYpos(MergeFinalNode.xpos()+300,MergeFinalNode.ypos()-25)
                                JpgFirstFrame = Read_JPG['first'].value()
                                JpgLastFrame = Read_JPG['last'].value()
                                JPG_FORMAT = Read_JPG['format'].value()
                                PixelAspectJPG = Read_JPG.pixelAspect()
                                MergeFinalNode.setInput(0,Read_JPG)
                            except:
                                pass 
                except:
                    nuke.message('Cannot find JPG')
                    pass
                
                CONES_FORMAT = CreateTree.ConesReadNode['format'].actualValue()
                CONES_WIDTH = CONES_FORMAT.width()
                CONES_HEIGHT = CONES_FORMAT.height()
                JPG_HEIGHT = JPG_FORMAT.height()
                JPG_WIDTH = JPG_FORMAT.width()
                
                Image_Aspect = JPG_WIDTH / JPG_HEIGHT
                if Image_Aspect > 2.0:
                    Anamorphic = True

                print ("Anamorphic = {}".format(Anamorphic))

                print ("CONES_FORMAT = {}".format(CONES_FORMAT))
                print ("CONES_WIDTH = {}".format(CONES_WIDTH))
                print ("CONES_HEIGHT = {}".format(CONES_HEIGHT))
                print ("JPG_HEIGHT = {}".format(JPG_HEIGHT))
                print ("JPG_WIDTH = {}".format(JPG_WIDTH))
                
                if Redist_Check == False and Undist_Check == False and LD_Check == False:
                    STMapNode['disable'].setValue(True)
                    print ("Undist and JPG are identical resolution")
                else:
                    print ("False equvalence")

            if StudioName == "Pixomondo":
        
                for x in nuke.allNodes():
                    x.setSelected(False)

                WireFrameProxyFolder = OriginalPreviewPath  + "proxy-jpg-wireframe"
                WireFrameProxyFolder = WireFrameProxyFolder.replace("\\","/")
                if not os.path.exists(WireFrameProxyFolder):
                    original_umask = os.umask(0)
                    os.makedirs(WireFrameProxyFolder,mode=0o777  )
                
                WireFrameEXRProxyFolder = OriginalPreviewPath  + "proxy-exr-wireframe"
                WireFrameEXRProxyFolder = WireFrameEXRProxyFolder.replace("\\","/")
                if not os.path.exists(WireFrameEXRProxyFolder):
                    original_umask = os.umask(0)
                    os.makedirs(WireFrameEXRProxyFolder,mode=0o777  ) 
                
                SpheresProxyFolder = OriginalPreviewPath  + "proxy-jpg-sphere"
                SpheresProxyFolder = SpheresProxyFolder.replace("\\","/")
                if not os.path.exists(SpheresProxyFolder):
                    original_umask = os.umask(0)
                    os.makedirs(SpheresProxyFolder,mode=0o777  ) 
                ConesProxyFolder = OriginalPreviewPath  + "proxy-jpg-cones"
                ConesProxyFolder = ConesProxyFolder.replace("\\","/")
                if not os.path.exists(ConesProxyFolder):
                    original_umask = os.umask(0)
                    os.makedirs(ConesProxyFolder,mode=0o777  ) 

                
                WriteWireFrameNode = nuke.nodes.Write()
                WriteWireFrameNode.setInput(0,MergeFinalNode)
                WriteWireFrameNode.setXYpos(MergeFinalNode.xpos(),MergeFinalNode.ypos()+100)
                WriteWireFrameNode["file"].setValue(WireFrameProxyFolder +"/" + ShotName + "." + Taraba +".jpg")
                WriteWireFrameNode['label'].setValue("WIREFRAME")
                WriteWireFrameNode['tile_color'].setValue(4287911423)
                try:
                    WriteWireFrameNode['file_type'].setValue("jpeg")
                    WriteWireFrameNode['_jpeg_quality'].setValue(1)
                except:
                    pass
            
                WriteWireFrameEXRNode = nuke.nodes.Write()
                WriteWireFrameEXRNode.setInput(0,MergeFinalNode)
                WriteWireFrameEXRNode.setXYpos(MergeFinalNode.xpos(),MergeFinalNode.ypos()+160)
                WriteWireFrameEXRNode["file"].setValue(WireFrameEXRProxyFolder +"/" + ShotName + "." + Taraba +".exr")
                WriteWireFrameEXRNode['label'].setValue("WIREFRAME_EXR")
                WriteWireFrameEXRNode['tile_color'].setValue(4283782655)
                try:
                    WriteWireFrameEXRNode['file_type'].setValue("exr")
                    WriteWireFrameEXRNode['datatype'].setValue(32)
                except:
                    pass
                WriteConesNode = nuke.nodes.Write()
                WriteConesNode.setInput(0,MergeFinalNode)
                WriteConesNode.setXYpos(MergeFinalNode.xpos()+100,MergeFinalNode.ypos()+100)
                WriteConesNode["file"].setValue(ConesProxyFolder +"/" + ShotName + "." + Taraba +".jpg")
                WriteConesNode['label'].setValue("CONES")
                WriteConesNode['tile_color'].setValue(1784020991)
                try:
                    WriteConesNode['file_type'].setValue("jpeg")
                    WriteConesNode['_jpeg_quality'].setValue(1)
                except:
                    pass
                WriteSpheresNode = nuke.nodes.Write()
                WriteSpheresNode.setInput(0,MergeFinalNode)
                WriteSpheresNode.setXYpos(MergeFinalNode.xpos()-100,MergeFinalNode.ypos()+100)
                WriteSpheresNode["file"].setValue(SpheresProxyFolder +"/" + ShotName +"." + Taraba +".jpg")
                WriteSpheresNode['label'].setValue("SPHERES")
                WriteSpheresNode['tile_color'].setValue(536805631)
                try:
                    WriteSpheresNode['file_type'].setValue("jpeg")
                    WriteSpheresNode['_jpeg_quality'].setValue(1)
                except:
                    pass
                CreateTree.RigErodeNode['disable'].setValue(False)
                CreateTree.RigColorCorrectNode.knob('gain').setValue(1,1)    #GREEN
                CreateTree.RigColorCorrectNode.knob('gain').setValue(0,2)    #BLUE

            elif StudioName == "Tippett":
                ReformatNode_HD = nuke.nodes.Reformat()
                ReformatNode_HD['name'].setValue("HDReformat")
                ReformatNode_HD['format'].setValue("HD_1080")
                ReformatNode_HD['resize'].setValue("width")
                ReformatNode_HD.setXYpos(Read_JPG.xpos(),Read_JPG.ypos()+120)
                ReformatNode_HD.setInput(0,Read_JPG)
                ReformatNode_HD.setSelected(True)
                try:
                    FocalLengthFile = ThreeD_comp_Path + "/main3d/" + "Focal Length.txt"
                    with open(FocalLengthFile) as focal:
                        FocalLengthText = focal.readlines()
                        #'FocalLength=29.02'
                        for line in FocalLengthText:
                            if "FocalLength" in line:
                                line = line.split("=")[-1]
                                FocalLength = line
                                print ("line = {}".format(line))
                        print ("FocalLengthText = {}".format(FocalLengthText))
                except:
                    pass

                for files in os.listdir(TippettPath):
                    if "_Slate" in files:
                        print ("Rig_Check = {}".format(Rig_Check)) 
                        TippettPathModified = TippettPath + files
                        TippettPath_SlateNode = nuke.nodePaste(TippettPathModified)
                        TippettPath_SlateNode.setXYpos(ReformatNode_HD.xpos(),ReformatNode_HD.ypos()+90)
                        TippettPath_SlateNode['project_name'].setValue(ProjectName)
                        try:
                            TippettPath_SlateNode['solved_lens'].setValue(FocalLength + "mm")
                        except:
                            pass
                        if Rig_Check == True:
                            TippettPath_SlateNode['note'].setValue("Camera,Rotomation")
                            print ("Rig_Camera")
                        else:
                            TippettPath_SlateNode['note'].setValue("Camera")
                        if LDCheck == True and UV_LD_Status == "LD Node":
                            TippettPath_SlateNode['ud_info'].setValue("3DELens")
                        else:
                            TippettPath_SlateNode['ud_info'].setValue("UVMaps")


                for files in os.listdir(TippettPath):
                    if "Burn" in files:
                        BurninPath = TippettPath + files
                        BurninNode = nuke.nodePaste(BurninPath)
                        BurninNode.setXYpos(MergeFinalNode.xpos(),MergeFinalNode.ypos()+90)
                        BurninNode.setInput(0,MergeFinalNode)
                    #    if Anamorphic == True:
                        BurninNode.begin()
                        Reformat2Node = nuke.toNode("Reformat2")
                        Reformat2Node['format'].setValue(JPG_FORMAT)
                        Constant2Node = nuke.toNode("Constant2")
                        Constant2Node['format'].setValue(JPG_FORMAT)
                        Studio_Text_Node = nuke.toNode("Studio_text")
                        Studio_Text_Node['box'].setValue(10,  0)
                        Studio_Text_Node['box'].setValue(JPG_HEIGHT-30,1)
                        Studio_Text_Node['box'].setValue(645, 2)
                        Studio_Text_Node['box'].setValue(JPG_HEIGHT,3)
                        Date_Text_Node = nuke.toNode("Date_text")
                        Date_Text_Node['box'].setValue(JPG_WIDTH-140,0)
                        Date_Text_Node['box'].setValue(JPG_HEIGHT-30,  1)
                        Date_Text_Node['box'].setValue(JPG_WIDTH,2)
                        Date_Text_Node['box'].setValue(JPG_HEIGHT,  3)
                        Frame_Text_Node = nuke.toNode("Frame_text")
                        Frame_Text_Node['box'].setValue(JPG_WIDTH-80, 0)
                        Frame_Text_Node['box'].setValue(33,   1)
                        Frame_Text_Node['box'].setValue(JPG_WIDTH, 2)
                        Frame_Text_Node['box'].setValue(33,   3)
                        ShotName_Text_Node = nuke.toNode("ShotName_text")
                        ShotName_Text_Node['box'].setValue(10, 0)
                        ShotName_Text_Node['box'].setValue(33,   1)
                        ShotName_Text_Node['box'].setValue(900, 2)
                        ShotName_Text_Node['box'].setValue(33,   3)
                        ShotName_Text_Node['message'].setValue("""[lindex [split [lindex [split [ lindex [split [knob [topnode this.parent.input].file] .] 0] /] end ] _ ] 0]_[lindex [split [lindex [split [ lindex [split [knob [topnode this.parent.input].file] .] 0] /] end ] _ ] 1]_[lindex [split [lindex [split [ lindex [split [knob [topnode this.parent.input].file] .] 0] /] end ] _ ] 2]""")
                        BurninNode.end()

                        SwitchNode = nuke.nodes.Switch()
                        SwitchNode.setInput(0,TippettPath_SlateNode)
                        SwitchNode.setInput(1,BurninNode)
                        SwitchNode.setXYpos(BurninNode.xpos(),BurninNode.ypos()+90)
                        SwitchNode['which'].setAnimated()
                        SwitchNode['which'].setValueAt(1,JpgFirstFrame)
                        SwitchNode['which'].setValueAt(0,JpgFirstFrame-1)
                for x in nuke.allNodes():
                    x.setSelected(False)

                def RemoveTipettPNG(node):
                    nuke.executeInMainThreadWithResult(nuke.execute, args = (node),kwargs = {'continueOnError': False})
                    print("......")
                
                #    for pngfiles in os.listdir(PreviewPath):
                #        if pngfiles.endswith(".png"):
                #            #os.delete(pngfiles)
                #            print(pngfiles)
                
                    
                
                def TipettRead():
                    print ("WritePath = {}".format(PreviewPath + RealPreviewFolder[0])) 
                    
                    for seq in nuke.getFileNameList(PreviewPath):
                        if ".png" in seq:
                            TippettPNGReadNode = nuke.nodes.Read()
                            TippettPNGReadNode.knob('file').fromUserText(PreviewPath + seq)
                    MOVWriteNode = nuke.nodes.Write()
                    MOVWriteNode.setInput(0,SwitchNode)
                    MOVWriteNode.setXYpos(WriteNode.xpos()-320,WriteNode.ypos())
                    MOVWriteNode["file"].setValue(PreviewPath + RealPreviewFolder[0] +".mov")
                    MOVWriteNode.setInput(0,TippettPNGReadNode)
                    MOVWriteNode["name"].setValue("MOVWriteNode")
                    TippettPNGReadNode.setXYpos(MOVWriteNode.xpos(),MOVWriteNode.ypos()-150)
                    TippettPNGReadNode["name"].setValue("TippettPNGReadNode")
                    thread = threading.Thread(None, RemoveTipettPNG, args= (MOVWriteNode,))
                    nuke.removeAfterRender(TipettRead)
                #    nuke.executeInMainThread(thread.start)
                    
                    
                    
                    
                    
                    
                WriteNode = nuke.nodes.Write()
                
            #    if Anamorphic == True:
                Final_HD_Reformat = nuke.nodes.Reformat()
                Final_HD_Reformat['name'].setValue("Final_HDReformat")
                Final_HD_Reformat['format'].setValue("HD_1080")
                Final_HD_Reformat['resize'].setValue("width")
                Final_HD_Reformat['black_outside'].setValue(True)
                Final_HD_Reformat['pbb'].setValue(True)
                Final_HD_Reformat.setXYpos(SwitchNode.xpos(),SwitchNode.ypos()+50)
                Final_HD_Reformat.setInput(0,SwitchNode)
                WriteNode.setInput(0,Final_HD_Reformat)
                WriteNode.setXYpos(SwitchNode.xpos(),SwitchNode.ypos()+120)
                WriteNode["file"].setValue(PreviewPath + RealPreviewFolder[0] +"." + Taraba +".png")
            #    else:
            #        WriteNode.setInput(0,SwitchNode)
            #        WriteNode.setXYpos(SwitchNode.xpos(),SwitchNode.ypos()+90)
            #        WriteNode["file"].setValue(PreviewPath + RealPreviewFolder[0] +"." + Taraba +".png")
            
            
            
            #    WriteNode["afterRender"].setValue(r"""for seq in nuke.getFileNameList("{PreviewPath}"):
            #            if ".png" in seq:
            #                TippettPNGReadNode = nuke.nodes.Read()
            #                TippettPNGReadNode.knob('file').fromUserText("{PreviewPath}" + "//" + seq)""".format(PreviewPath=PreviewPath))
            #    nuke.addAfterRender(TipettRead)
                
                try:
                    WriteNode['file_type'].setValue("png")
                    WriteNode['datatype'].setValue("16 Bit")
                except:
                    pass

                FrameRange = ("{}-{}".format(JpgFirstFrame-1,JpgLastFrame))
                print ("FrameRange = {}".format(FrameRange)) 
                nukescripts.renderdialog._gRenderDialogState.saveValue('frame_range', 'custom')
                nukescripts.renderdialog._gRenderDialogState.saveValue('frame_range_string', FrameRange)
            else:
        
                for x in nuke.allNodes():
                    x.setSelected(False)

            #    WriteNode.setSelected(True)
            #    nuke.toNode("Write1").setSelected(True)
                WriteNode = nuke.nodes.Write()
                WriteNode.setInput(0,MergeFinalNode)
                WriteNode.setXYpos(MergeFinalNode.xpos(),MergeFinalNode.ypos()+100)
                WriteNode["file"].setValue(PreviewPath + RealPreviewFolder[0] + "." + Taraba +".jpg")
                try:
                    WriteNode['file_type'].setValue("jpeg")
                    WriteNode['_jpeg_quality'].setValue(1)
                except:
                    pass


        elif Cones_Check == False and Geo_Check == True:
            print ("No Cones, only Geo")
            MergeTreesNode.setXYpos(CreateTree.GeoMergeNode.xpos(),CreateTree.GeoMergeNode.ypos()+80)
            MergeTreesNode.setInput(1,CreateTree.GeoMergeNode)
            MergeTreesNode.setXYpos(CreateTree.GeoMergeNode.xpos(),CreateTree.GeoMergeNode.ypos()+100)
            MergeTreesNode['label'].setValue("ALL")
            BlurAllNode = nuke.createNode("Blur")
            BlurAllNode.setXYpos(MergeTreesNode.xpos(),MergeTreesNode.ypos()+80)
            BlurAllNode.setInput(0,MergeTreesNode)
            BlurAllNode["size"].setValue(1.2)
            # IF this is an LD node type of shot
            if LDCheck == True and UV_LD_Status == "LD Node" :
                try:
                    for seq in nuke.getFileNameList(JPGPath):
                        Split = seq.split(" ")
                        Split.pop()
                        Split = "".join(Split)
                        if Split.endswith(".jpg"):
                            Read_JPG = nuke.createNode('Read')
                            Read_JPG.knob('file').fromUserText(JPGPath + seq)
                            JpgFirstFrame = Read_JPG['first'].value()
                            JpgLastFrame = Read_JPG['last'].value()
                            JPG_FORMAT = Read_JPG['format'].value()
                            PixelAspectJPG = Read_JPG.pixelAspect()
                            ReformatLDNode = nuke.nodes.Reformat()
                            ReformatLDNode['format'].setValue(JPG_FORMAT)
                            ReformatLDNode['black_outside'].setValue(True)
                            ReformatLDNode['pbb'].setValue(True)
                            ReformatLDNode['resize'].setValue("none")
                            ReformatLDNode.setXYpos(BlurAllNode.xpos(),BlurAllNode.ypos()+80)
                            ReformatLDNode.setInput(0,BlurAllNode)
                            
                except:
                    nuke.message('Cannot find JPG')
                    pass

                for LD in os.listdir(LDNodePath):
                    if "dist_".lower() in LD.lower():
                        Split,ext = os.path.splitext(LD)
                        SplitDist = Split.split("_")
                        for v in SplitDist:
                            if "v0" in v:
                                LastVersion = v
                                
                    try:
                        LastVersion
                    except NameError:
                        pass
                for LD in os.listdir(LDNodePath):
                    try:
                        if "dist_{}".format(LastVersion).lower() in LD.lower():
                            LDNodePath = LDNodePath + LD
                            LDNode = nuke.nodePaste(LDNodePath)
                            LDNode['direction'].setValue("distort")
                            LDNode['name'].setValue(LDNode.name() + "_" + LastVersion)
                            LDNode.setInput(0,ReformatLDNode)
                            LDNode.setXYpos(ReformatLDNode.xpos(),ReformatLDNode.ypos()+80)
                            MergeFinalNode = nuke.nodes.Merge2()
                            MergeFinalNode.setXYpos(LDNode.xpos(),LDNode.ypos()+120)
                            MergeFinalNode.setInput(1,LDNode)
                            MergeFinalNode["name"].setValue("Merge")
                            MergeFinalNode["label"].setValue("FINAL")
                            MergeFinalNode.setInput(0,Read_JPG)
                            Read_JPG.setXYpos(MergeFinalNode.xpos()+300,MergeFinalNode.ypos()-25)
                    except:
                            pass
                GEO_FORMAT = CreateTree.GeoReadNode['format'].actualValue()
                GEO_WIDTH = GEO_FORMAT.width()
                GEO_HEIGHT = GEO_FORMAT.height()
                JPG_HEIGHT = JPG_FORMAT.height()
                JPG_WIDTH = JPG_FORMAT.width()
                Image_Aspect = JPG_WIDTH / JPG_HEIGHT
                if Image_Aspect > 2.0:
                    Anamorphic = True

                print ("Anamorphic = {}".format(Anamorphic))

                print ("GEO_FORMAT = {}".format(GEO_FORMAT))
                print ("GEO_WIDTH = {}".format(GEO_WIDTH))
                print ("GEO_HEIGHT = {}".format(GEO_HEIGHT))
                print ("JPG_HEIGHT = {}".format(JPG_HEIGHT))
                print ("JPG_WIDTH = {}".format(JPG_WIDTH))
            #IF it is a UV MAP type of shot
            else:
                for uv in nuke.getFileNameList(UVDistortPath):
                    print (uv)
                    try:
                        if "redi" in uv.lower():
                            Read_RedistortEXR = nuke.createNode('Read')
                            Read_RedistortEXR.knob('file').fromUserText(UVDistortPath + uv)
            
                    except:
                        nuke.message("Missing Redist Map, name it 'redist' ")
                        pass
                STMapNode = nuke.nodes.STMap (uv="rgba")
                STMapNode.setInput(0,BlurAllNode)
                #    STMapNode.setInput(1,RedistNode)
                STMapNode.setXYpos(BlurAllNode.xpos(),BlurAllNode.ypos()+80)
                try:
                    STMapNode.setInput(1,Read_RedistortEXR)
                except:
                    pass
                try:
                    Read_RedistortEXR.setXYpos(STMapNode.xpos()+150,STMapNode.ypos()-25)
                except:
                    pass
                MergeFinalNode = nuke.nodes.Merge2()
                MergeFinalNode.setXYpos(STMapNode.xpos(),STMapNode.ypos()+120)
        #        MergeFinalNode.setInput(0,STMapNode)
                MergeFinalNode.setInput(1,STMapNode)
                MergeFinalNode["name"].setValue("Merge")
                MergeFinalNode["label"].setValue("FINAL")

                try:
                    for seq in nuke.getFileNameList(JPGPath):
                        Split = seq.split(" ")
                        Split.pop()
                        Split = "".join(Split)
                        if Split.endswith(".jpg"):
                            Read_JPG = nuke.createNode('Read')
                            try:
                                Read_JPG.knob('file').fromUserText(JPGPath + seq)
                                Read_JPG.setXYpos(MergeFinalNode.xpos()+300,MergeFinalNode.ypos()-25)
                                JpgFirstFrame = Read_JPG['first'].value()
                                JpgLastFrame = Read_JPG['last'].value()
                                JPG_FORMAT = Read_JPG['format'].value()
                                PixelAspectJPG = Read_JPG.pixelAspect()
                                MergeFinalNode.setInput(0,Read_JPG)
                            except:
                                pass 
                except:
                    nuke.message('Cannot find JPG')
                    pass
                
                GEO_FORMAT = CreateTree.GeoReadNode['format'].actualValue()
                GEO_WIDTH = GEO_FORMAT.width()
                GEO_HEIGHT = GEO_FORMAT.height()
                JPG_HEIGHT = JPG_FORMAT.height()
                JPG_WIDTH = JPG_FORMAT.width()
                Image_Aspect = JPG_WIDTH / JPG_HEIGHT
                if Image_Aspect > 2.0:
                    Anamorphic = True

                print ("Anamorphic = {}".format(Anamorphic))
                print ("GEO_FORMAT = {}".format(GEO_FORMAT))
                print ("GEO_WIDTH = {}".format(GEO_WIDTH))
                print ("GEO_HEIGHT = {}".format(GEO_HEIGHT))
                print ("JPG_HEIGHT = {}".format(JPG_HEIGHT))
                print ("JPG_WIDTH = {}".format(JPG_WIDTH))
                
                if Redist_Check == False and Undist_Check == False and LD_Check == False:
                    STMapNode['disable'].setValue(True)
                    print ("Undist and JPG are identical resolution")
                else:
                    print ("False equvalence")
            
            if StudioName == "Pixomondo":

                for x in nuke.allNodes():
                    x.setSelected(False)

                WireFrameProxyFolder = OriginalPreviewPath  + "proxy-jpg-wireframe"
                WireFrameProxyFolder = WireFrameProxyFolder.replace("\\","/")
                if not os.path.exists(WireFrameProxyFolder):
                    original_umask = os.umask(0)
                    os.makedirs(WireFrameProxyFolder,mode=0o777  )
                
                WireFrameEXRProxyFolder = OriginalPreviewPath  + "proxy-exr-wireframe"
                WireFrameEXRProxyFolder = WireFrameEXRProxyFolder.replace("\\","/")
                if not os.path.exists(WireFrameEXRProxyFolder):
                    original_umask = os.umask(0)
                    os.makedirs(WireFrameEXRProxyFolder,mode=0o777  ) 
                
                SpheresProxyFolder = OriginalPreviewPath  + "proxy-jpg-sphere"
                SpheresProxyFolder = SpheresProxyFolder.replace("\\","/")
                if not os.path.exists(SpheresProxyFolder):
                    original_umask = os.umask(0)
                    os.makedirs(SpheresProxyFolder,mode=0o777  ) 
                ConesProxyFolder = OriginalPreviewPath  + "proxy-jpg-cones"
                ConesProxyFolder = ConesProxyFolder.replace("\\","/")
                if not os.path.exists(ConesProxyFolder):
                    original_umask = os.umask(0)
                    os.makedirs(ConesProxyFolder,mode=0o777  ) 

                
                WriteWireFrameNode = nuke.nodes.Write()
                WriteWireFrameNode.setInput(0,MergeFinalNode)
                WriteWireFrameNode.setXYpos(MergeFinalNode.xpos(),MergeFinalNode.ypos()+100)
                WriteWireFrameNode["file"].setValue(WireFrameProxyFolder +"/" + ShotName + "." + Taraba +".jpg")
                WriteWireFrameNode['label'].setValue("WIREFRAME")
                WriteWireFrameNode['tile_color'].setValue(4287911423)
                try:
                    WriteWireFrameNode['file_type'].setValue("jpeg")
                    WriteWireFrameNode['_jpeg_quality'].setValue(1)
                except:
                    pass
            
                WriteWireFrameEXRNode = nuke.nodes.Write()
                WriteWireFrameEXRNode.setInput(0,MergeFinalNode)
                WriteWireFrameEXRNode.setXYpos(MergeFinalNode.xpos(),MergeFinalNode.ypos()+160)
                WriteWireFrameEXRNode["file"].setValue(WireFrameEXRProxyFolder +"/" + ShotName + "." + Taraba +".exr")
                WriteWireFrameEXRNode['label'].setValue("WIREFRAME_EXR")
                WriteWireFrameEXRNode['tile_color'].setValue(4283782655)
                try:
                    WriteWireFrameEXRNode['file_type'].setValue("exr")
                    WriteWireFrameEXRNode['datatype'].setValue(32)
                except:
                    pass
                WriteConesNode = nuke.nodes.Write()
                WriteConesNode.setInput(0,MergeFinalNode)
                WriteConesNode.setXYpos(MergeFinalNode.xpos()+100,MergeFinalNode.ypos()+100)
                WriteConesNode["file"].setValue(ConesProxyFolder +"/" + ShotName + "." + Taraba +".jpg")
                WriteConesNode['label'].setValue("CONES")
                WriteConesNode['tile_color'].setValue(1784020991)
                try:
                    WriteConesNode['file_type'].setValue("jpeg")
                    WriteConesNode['_jpeg_quality'].setValue(1)
                except:
                    pass
                WriteSpheresNode = nuke.nodes.Write()
                WriteSpheresNode.setInput(0,MergeFinalNode)
                WriteSpheresNode.setXYpos(MergeFinalNode.xpos()-100,MergeFinalNode.ypos()+100)
                WriteSpheresNode["file"].setValue(SpheresProxyFolder +"/" + ShotName +"." + Taraba +".jpg")
                WriteSpheresNode['label'].setValue("SPHERES")
                WriteSpheresNode['tile_color'].setValue(536805631)
                try:
                    WriteSpheresNode['file_type'].setValue("jpeg")
                    WriteSpheresNode['_jpeg_quality'].setValue(1)
                except:
                    pass
                CreateTree.RigErodeNode['disable'].setValue(False)
                CreateTree.RigColorCorrectNode.knob('gain').setValue(1,1)    #GREEN
                CreateTree.RigColorCorrectNode.knob('gain').setValue(0,2)    #BLUE

            elif StudioName == "Tippett":
                ReformatNode_HD = nuke.nodes.Reformat()
                ReformatNode_HD['name'].setValue("HDReformat")
                ReformatNode_HD['format'].setValue("HD_1080")
                ReformatNode_HD['resize'].setValue("width")
                ReformatNode_HD.setXYpos(Read_JPG.xpos(),Read_JPG.ypos()+120)
                ReformatNode_HD.setInput(0,Read_JPG)
                ReformatNode_HD.setSelected(True)
                try:
                    FocalLengthFile = ThreeD_comp_Path + "/main3d/" + "Focal Length.txt"
                    with open(FocalLengthFile) as focal:
                        FocalLengthText = focal.readlines()
                        #'FocalLength=29.02'
                        for line in FocalLengthText:
                            if "FocalLength" in line:
                                line = line.split("=")[-1]
                                FocalLength = line
                                print ("line = {}".format(line))
                        print ("FocalLengthText = {}".format(FocalLengthText))
                except:
                    pass

                for files in os.listdir(TippettPath):
                    if "_Slate" in files:
                        print ("Rig_Check = {}".format(Rig_Check)) 
                        TippettPathModified = TippettPath + files
                        TippettPath_SlateNode = nuke.nodePaste(TippettPathModified)
                        TippettPath_SlateNode.setXYpos(ReformatNode_HD.xpos(),ReformatNode_HD.ypos()+90)
                        TippettPath_SlateNode['project_name'].setValue(ProjectName)
                        try:
                            TippettPath_SlateNode['solved_lens'].setValue(FocalLength + "mm")
                        except:
                            pass
                        if Rig_Check == True:
                            TippettPath_SlateNode['note'].setValue("Camera,Rotomation")
                            print ("Rig_Camera")
                        else:
                            TippettPath_SlateNode['note'].setValue("Camera")
                        if LDCheck == True and UV_LD_Status == "LD Node":
                            TippettPath_SlateNode['ud_info'].setValue("3DELens")
                        else:
                            TippettPath_SlateNode['ud_info'].setValue("UVMaps")


                for files in os.listdir(TippettPath):
                    if "Burn" in files:
                        BurninPath = TippettPath + files
                        BurninNode = nuke.nodePaste(BurninPath)
                        BurninNode.setXYpos(MergeFinalNode.xpos(),MergeFinalNode.ypos()+90)
                        BurninNode.setInput(0,MergeFinalNode)
                    #    if Anamorphic == True:
                        BurninNode.begin()
                        Reformat2Node = nuke.toNode("Reformat2")
                        Reformat2Node['format'].setValue(JPG_FORMAT)
                        Constant2Node = nuke.toNode("Constant2")
                        Constant2Node['format'].setValue(JPG_FORMAT)
                        Studio_Text_Node = nuke.toNode("Studio_text")
                        Studio_Text_Node['box'].setValue(10,  0)
                        Studio_Text_Node['box'].setValue(JPG_HEIGHT-30,1)
                        Studio_Text_Node['box'].setValue(645, 2)
                        Studio_Text_Node['box'].setValue(JPG_HEIGHT,3)
                        Date_Text_Node = nuke.toNode("Date_text")
                        Date_Text_Node['box'].setValue(JPG_WIDTH-140,0)
                        Date_Text_Node['box'].setValue(JPG_HEIGHT-30,  1)
                        Date_Text_Node['box'].setValue(JPG_WIDTH,2)
                        Date_Text_Node['box'].setValue(JPG_HEIGHT,  3)
                        Frame_Text_Node = nuke.toNode("Frame_text")
                        Frame_Text_Node['box'].setValue(JPG_WIDTH-80, 0)
                        Frame_Text_Node['box'].setValue(33,   1)
                        Frame_Text_Node['box'].setValue(JPG_WIDTH, 2)
                        Frame_Text_Node['box'].setValue(33,   3)
                        ShotName_Text_Node = nuke.toNode("ShotName_text")
                        ShotName_Text_Node['box'].setValue(10, 0)
                        ShotName_Text_Node['box'].setValue(33,   1)
                        ShotName_Text_Node['box'].setValue(900, 2)
                        ShotName_Text_Node['box'].setValue(33,   3)
                        ShotName_Text_Node['message'].setValue("""[lindex [split [lindex [split [ lindex [split [knob [topnode this.parent.input].file] .] 0] /] end ] _ ] 0]_[lindex [split [lindex [split [ lindex [split [knob [topnode this.parent.input].file] .] 0] /] end ] _ ] 1]_[lindex [split [lindex [split [ lindex [split [knob [topnode this.parent.input].file] .] 0] /] end ] _ ] 2]""")
                        BurninNode.end()
                        SwitchNode = nuke.nodes.Switch()
                        SwitchNode.setInput(0,TippettPath_SlateNode)
                        SwitchNode.setInput(1,BurninNode)
                        SwitchNode.setXYpos(BurninNode.xpos(),BurninNode.ypos()+90)
                        SwitchNode['which'].setAnimated()
                        SwitchNode['which'].setValueAt(1,JpgFirstFrame)
                        SwitchNode['which'].setValueAt(0,JpgFirstFrame-1)
                for x in nuke.allNodes():
                    x.setSelected(False)
                WriteNode = nuke.nodes.Write()
                
                Final_HD_Reformat = nuke.nodes.Reformat()
                Final_HD_Reformat['name'].setValue("Final_HDReformat")
                Final_HD_Reformat['format'].setValue("HD_1080")
                Final_HD_Reformat['resize'].setValue("width")
                Final_HD_Reformat['black_outside'].setValue(True)
                Final_HD_Reformat['pbb'].setValue(True)
                Final_HD_Reformat.setXYpos(SwitchNode.xpos(),SwitchNode.ypos()+50)
                Final_HD_Reformat.setInput(0,SwitchNode)
                WriteNode.setInput(0,Final_HD_Reformat)
                WriteNode.setXYpos(SwitchNode.xpos(),SwitchNode.ypos()+120)
                WriteNode["file"].setValue(PreviewPath + RealPreviewFolder[0] +"." + Taraba +".png")

                
                try:
                    WriteNode['file_type'].setValue("png")
                    WriteNode['datatype'].setValue("16 Bit")
                except:
                    pass
                FrameRange = ("{}-{}".format(JpgFirstFrame-1,JpgLastFrame))
                print ("FrameRange = {}".format(FrameRange)) 
                nukescripts.renderdialog._gRenderDialogState.saveValue('frame_range', 'custom')
                nukescripts.renderdialog._gRenderDialogState.saveValue('frame_range_string', FrameRange)
            else:
                for x in nuke.allNodes():
                    x.setSelected(False)

            #    WriteNode.setSelected(True)
            #    nuke.toNode("Write1").setSelected(True)
                WriteNode = nuke.nodes.Write()
                WriteNode.setInput(0,MergeFinalNode)
                WriteNode.setXYpos(MergeFinalNode.xpos(),MergeFinalNode.ypos()+100)

                WriteNode["file"].setValue(PreviewPath + RealPreviewFolder[0] + "." + Taraba +".jpg")
                WriteNode['name'].setValue(ShotName + " WriteNode")
                try:
                    WriteNode['file_type'].setValue("jpeg")
                    WriteNode['_jpeg_quality'].setValue(1)
                except:
                    pass

        
    
        elif Cones_Check == False and Geo_Check == False and Rig_Check == True:
            print ("No Cones or Geo, just Rig")
            MergeTreesNode.setInput(1,CreateTree.RigMergeNode)
            MergeTreesNode.setXYpos(CreateTree.RigMergeNode.xpos(),CreateTree.RigMergeNode.ypos()+100)
            MergeTreesNode['label'].setValue("ALL")
            BlurAllNode = nuke.createNode("Blur")
            BlurAllNode.setXYpos(MergeTreesNode.xpos(),MergeTreesNode.ypos()+80)
            BlurAllNode.setInput(0,MergeTreesNode)
            BlurAllNode["size"].setValue(1.2)
            # IF this is an LD node type of shot
            if LDCheck == True and UV_LD_Status == "LD Node" :
                try:
                    for seq in nuke.getFileNameList(JPGPath):
                        Split = seq.split(" ")
                        Split.pop()
                        Split = "".join(Split)
                        if Split.endswith(".jpg"):
                            Read_JPG = nuke.createNode('Read')
                            Read_JPG.knob('file').fromUserText(JPGPath + seq)
                            JpgFirstFrame = Read_JPG['first'].value()
                            JpgLastFrame = Read_JPG['last'].value()
                            JPG_FORMAT = Read_JPG['format'].value()
                            PixelAspectJPG = Read_JPG.pixelAspect()
                            ReformatLDNode = nuke.nodes.Reformat()
                            ReformatLDNode['format'].setValue(JPG_FORMAT)
                            ReformatLDNode['black_outside'].setValue(True)
                            ReformatLDNode['pbb'].setValue(True)
                            ReformatLDNode['resize'].setValue("none")
                            ReformatLDNode.setXYpos(BlurAllNode.xpos(),BlurAllNode.ypos()+80)
                            ReformatLDNode.setInput(0,BlurAllNode)
                            
                except:
                    nuke.message('Cannot find JPG')
                    pass

                for LD in os.listdir(LDNodePath):
                    if "dist_".lower() in LD.lower():
                        Split,ext = os.path.splitext(LD)
                        SplitDist = Split.split("_")
                        for v in SplitDist:
                            if "v0" in v:
                                LastVersion = v
                                
                    try:
                        LastVersion
                    except NameError:
                        pass
                for LD in os.listdir(LDNodePath):
                    try:
                        if "dist_{}".format(LastVersion).lower() in LD.lower():
                            LDNodePath = LDNodePath + LD
                            LDNode = nuke.nodePaste(LDNodePath)
                            LDNode['direction'].setValue("distort")
                            LDNode['name'].setValue(LDNode.name() + "_" + LastVersion)
                            LDNode.setInput(0,ReformatLDNode)
                            LDNode.setXYpos(ReformatLDNode.xpos(),ReformatLDNode.ypos()+80)
                            MergeFinalNode = nuke.nodes.Merge2()
                            MergeFinalNode.setXYpos(LDNode.xpos(),LDNode.ypos()+120)
                            MergeFinalNode.setInput(1,LDNode)
                            MergeFinalNode["name"].setValue("Merge")
                            MergeFinalNode["label"].setValue("FINAL")
                            MergeFinalNode.setInput(0,Read_JPG)
                            Read_JPG.setXYpos(MergeFinalNode.xpos()+300,MergeFinalNode.ypos()-25)
                    except:
                            pass
                RIG_FORMAT = CreateTree.RigReadNode['format'].actualValue()
                RIG_WIDTH = RIG_FORMAT.width()
                RIG_HEIGHT = RIG_FORMAT.height()
                JPG_HEIGHT = JPG_FORMAT.height()
                JPG_WIDTH = JPG_FORMAT.width()

                Image_Aspect = JPG_WIDTH / JPG_HEIGHT
                if Image_Aspect > 2.0:
                    Anamorphic = True

                print ("Anamorphic = {}".format(Anamorphic))
                print ("RIG_FORMAT = {}".format(RIG_FORMAT))
                print ("RIG_WIDTH = {}".format(RIG_WIDTH))
                print ("RIG_HEIGHT = {}".format(RIG_HEIGHT))
                print ("JPG_HEIGHT = {}".format(JPG_HEIGHT))
                print ("JPG_WIDTH = {}".format(JPG_WIDTH))
            #IF it is a UV MAP type of shot
            else:
                for uv in nuke.getFileNameList(UVDistortPath):
                    print (uv)
                    try:
                        if "redi" in uv.lower():
                            Read_RedistortEXR = nuke.createNode('Read')
                            Read_RedistortEXR.knob('file').fromUserText(UVDistortPath + uv)
            
                    except:
                        nuke.message("Missing Redist Map, name it 'redist' ")
                        pass
                STMapNode = nuke.nodes.STMap (uv="rgba")
                STMapNode.setInput(0,BlurAllNode)
                #    STMapNode.setInput(1,RedistNode)
                STMapNode.setXYpos(BlurAllNode.xpos(),BlurAllNode.ypos()+80)
                try:
                    STMapNode.setInput(1,Read_RedistortEXR)
                except:
                    nuke.message('Cannot find Redist Map')
                    print ("Cannot find Redist Map")
                try:
                    Read_RedistortEXR.setXYpos(STMapNode.xpos()+150,STMapNode.ypos()-25)
                except:
                    pass
                MergeFinalNode = nuke.nodes.Merge2()
                MergeFinalNode.setXYpos(STMapNode.xpos(),STMapNode.ypos()+120)
        #        MergeFinalNode.setInput(0,STMapNode)
                MergeFinalNode.setInput(1,STMapNode)
                MergeFinalNode["name"].setValue("Merge")
                MergeFinalNode["label"].setValue("FINAL")

                try:
                    for seq in nuke.getFileNameList(JPGPath):
                        Split = seq.split(" ")
                        Split.pop()
                        Split = "".join(Split)
                        if Split.endswith(".jpg"):
                            Read_JPG = nuke.createNode('Read')
                            try:
                                Read_JPG.knob('file').fromUserText(JPGPath + seq)
                                Read_JPG.setXYpos(MergeFinalNode.xpos()+300,MergeFinalNode.ypos()-25)
                                JpgFirstFrame = Read_JPG['first'].value()
                                JpgLastFrame = Read_JPG['last'].value()
                                JPG_FORMAT = Read_JPG['format'].value()
                                PixelAspectJPG = Read_JPG.pixelAspect()
                                MergeFinalNode.setInput(0,Read_JPG)
                            except:
                                pass 
                except:
                    nuke.message('Cannot find JPG')
                    pass
                
                RIG_FORMAT = CreateTree.ConesReadNode['format'].actualValue()
                RIG_WIDTH = RIG_FORMAT.width()
                RIG_HEIGHT = RIG_FORMAT.height()
                JPG_HEIGHT = JPG_FORMAT.height()
                JPG_WIDTH = JPG_FORMAT.width()

                Image_Aspect = JPG_WIDTH / JPG_HEIGHT
                if Image_Aspect > 2.0:
                    Anamorphic = True

                print ("Anamorphic = {}".format(Anamorphic))
                print ("RIG_FORMAT = {}".format(RIG_FORMAT))
                print ("RIG_WIDTH = {}".format(RIG_WIDTH))
                print ("RIG_HEIGHT = {}".format(RIG_HEIGHT))
                print ("JPG_HEIGHT = {}".format(JPG_HEIGHT))
                print ("JPG_WIDTH = {}".format(JPG_WIDTH))
                
                if Redist_Check == False and Undist_Check == False and LD_Check == False:
                    STMapNode['disable'].setValue(True)
                    print ("Undist and JPG are identical resolution")
                else:
                    print ("False equvalence")
            if StudioName == "Pixomondo":
        
                for x in nuke.allNodes():
                    x.setSelected(False)

                WireFrameProxyFolder = OriginalPreviewPath  + "proxy-jpg-wireframe"
                WireFrameProxyFolder = WireFrameProxyFolder.replace("\\","/")
                if not os.path.exists(WireFrameProxyFolder):
                    original_umask = os.umask(0)
                    os.makedirs(WireFrameProxyFolder,mode=0o777  )
                
                WireFrameEXRProxyFolder = OriginalPreviewPath  + "proxy-exr-wireframe"
                WireFrameEXRProxyFolder = WireFrameEXRProxyFolder.replace("\\","/")
                if not os.path.exists(WireFrameEXRProxyFolder):
                    original_umask = os.umask(0)
                    os.makedirs(WireFrameEXRProxyFolder,mode=0o777  ) 
                
                SpheresProxyFolder = OriginalPreviewPath  + "proxy-jpg-sphere"
                SpheresProxyFolder = SpheresProxyFolder.replace("\\","/")
                if not os.path.exists(SpheresProxyFolder):
                    original_umask = os.umask(0)
                    os.makedirs(SpheresProxyFolder,mode=0o777  ) 
                ConesProxyFolder = OriginalPreviewPath  + "proxy-jpg-cones"
                ConesProxyFolder = ConesProxyFolder.replace("\\","/")
                if not os.path.exists(ConesProxyFolder):
                    original_umask = os.umask(0)
                    os.makedirs(ConesProxyFolder,mode=0o777  ) 

                
                WriteWireFrameNode = nuke.nodes.Write()
                WriteWireFrameNode.setInput(0,MergeFinalNode)
                WriteWireFrameNode.setXYpos(MergeFinalNode.xpos(),MergeFinalNode.ypos()+100)
                WriteWireFrameNode["file"].setValue(WireFrameProxyFolder +"/" + ShotName + "." + Taraba +".jpg")
                WriteWireFrameNode['label'].setValue("WIREFRAME")
                WriteWireFrameNode['tile_color'].setValue(4287911423)
                try:
                    WriteWireFrameNode['file_type'].setValue("jpeg")
                    WriteWireFrameNode['_jpeg_quality'].setValue(1)
                except:
                    pass
            
                WriteWireFrameEXRNode = nuke.nodes.Write()
                WriteWireFrameEXRNode.setInput(0,MergeFinalNode)
                WriteWireFrameEXRNode.setXYpos(MergeFinalNode.xpos(),MergeFinalNode.ypos()+160)
                WriteWireFrameEXRNode["file"].setValue(WireFrameEXRProxyFolder +"/" + ShotName + "." + Taraba +".exr")
                WriteWireFrameEXRNode['label'].setValue("WIREFRAME_EXR")
                WriteWireFrameEXRNode['tile_color'].setValue(4283782655)
                try:
                    WriteWireFrameEXRNode['file_type'].setValue("exr")
                    WriteWireFrameEXRNode['datatype'].setValue(32)
                except:
                    pass
                WriteConesNode = nuke.nodes.Write()
                WriteConesNode.setInput(0,MergeFinalNode)
                WriteConesNode.setXYpos(MergeFinalNode.xpos()+100,MergeFinalNode.ypos()+100)
                WriteConesNode["file"].setValue(ConesProxyFolder +"/" + ShotName + "." + Taraba +".jpg")
                WriteConesNode['label'].setValue("CONES")
                WriteConesNode['tile_color'].setValue(1784020991)
                try:
                    WriteConesNode['file_type'].setValue("jpeg")
                    WriteConesNode['_jpeg_quality'].setValue(1)
                except:
                    pass
                WriteSpheresNode = nuke.nodes.Write()
                WriteSpheresNode.setInput(0,MergeFinalNode)
                WriteSpheresNode.setXYpos(MergeFinalNode.xpos()-100,MergeFinalNode.ypos()+100)
                WriteSpheresNode["file"].setValue(SpheresProxyFolder +"/" + ShotName +"." + Taraba +".jpg")
                WriteSpheresNode['label'].setValue("SPHERES")
                WriteSpheresNode['tile_color'].setValue(536805631)
                try:
                    WriteSpheresNode['file_type'].setValue("jpeg")
                    WriteSpheresNode['_jpeg_quality'].setValue(1)
                except:
                    pass
                CreateTree.RigErodeNode['disable'].setValue(False)
                CreateTree.RigColorCorrectNode.knob('gain').setValue(1,1)    #GREEN
                CreateTree.RigColorCorrectNode.knob('gain').setValue(0,2)    #BLUE

            elif StudioName == "Tippett":
                ReformatNode_HD = nuke.nodes.Reformat()
                ReformatNode_HD['name'].setValue("HDReformat")
                ReformatNode_HD['format'].setValue("HD_1080")
                ReformatNode_HD['resize'].setValue("width")
                ReformatNode_HD.setXYpos(Read_JPG.xpos(),Read_JPG.ypos()+120)
                ReformatNode_HD.setInput(0,Read_JPG)
                ReformatNode_HD.setSelected(True)
                try:
                    FocalLengthFile = ThreeD_comp_Path + "/main3d/" + "Focal Length.txt"
                    with open(FocalLengthFile) as focal:
                        FocalLengthText = focal.readlines()
                        #'FocalLength=29.02'
                        for line in FocalLengthText:
                            if "FocalLength" in line:
                                line = line.split("=")[-1]
                                FocalLength = line
                                print ("line = {}".format(line))
                        print ("FocalLengthText = {}".format(FocalLengthText))
                except:
                    pass
                
                for files in os.listdir(TippettPath):
                    if "_Slate" in files:
                        print ("Rig_Check = {}".format(Rig_Check)) 
                        TippettPathModified = TippettPath + files
                        TippettPath_SlateNode = nuke.nodePaste(TippettPathModified)
                        TippettPath_SlateNode.setXYpos(ReformatNode_HD.xpos(),ReformatNode_HD.ypos()+90)
                        TippettPath_SlateNode['project_name'].setValue(ProjectName)
                        try:
                            TippettPath_SlateNode['solved_lens'].setValue(FocalLength + "mm")
                        except:
                            pass
                        if Rig_Check == True:
                            TippettPath_SlateNode['note'].setValue("Camera,Rotomation")
                            print ("Rig_Camera")
                        else:
                            TippettPath_SlateNode['note'].setValue("Camera")
                        if LDCheck == True and UV_LD_Status == "LD Node":
                            TippettPath_SlateNode['ud_info'].setValue("3DELens")
                        else:
                            TippettPath_SlateNode['ud_info'].setValue("UVMaps")


                for files in os.listdir(TippettPath):
                    if "Burn" in files:
                        BurninPath = TippettPath + files
                        BurninNode = nuke.nodePaste(BurninPath)
                        BurninNode.setXYpos(MergeFinalNode.xpos(),MergeFinalNode.ypos()+90)
                        BurninNode.setInput(0,MergeFinalNode)
                    #    if Anamorphic == True:
                        BurninNode.begin()
                        Reformat2Node = nuke.toNode("Reformat2")
                        Reformat2Node['format'].setValue(JPG_FORMAT)
                        Constant2Node = nuke.toNode("Constant2")
                        Constant2Node['format'].setValue(JPG_FORMAT)
                        Studio_Text_Node = nuke.toNode("Studio_text")
                        Studio_Text_Node['box'].setValue(10,  0)
                        Studio_Text_Node['box'].setValue(JPG_HEIGHT-30,1)
                        Studio_Text_Node['box'].setValue(645, 2)
                        Studio_Text_Node['box'].setValue(JPG_HEIGHT,3)
                        Date_Text_Node = nuke.toNode("Date_text")
                        Date_Text_Node['box'].setValue(JPG_WIDTH-140,0)
                        Date_Text_Node['box'].setValue(JPG_HEIGHT-30,  1)
                        Date_Text_Node['box'].setValue(JPG_WIDTH,2)
                        Date_Text_Node['box'].setValue(JPG_HEIGHT,  3)
                        Frame_Text_Node = nuke.toNode("Frame_text")
                        Frame_Text_Node['box'].setValue(JPG_WIDTH-80, 0)
                        Frame_Text_Node['box'].setValue(33,   1)
                        Frame_Text_Node['box'].setValue(JPG_WIDTH, 2)
                        Frame_Text_Node['box'].setValue(33,   3)
                        ShotName_Text_Node = nuke.toNode("ShotName_text")
                        ShotName_Text_Node['box'].setValue(10, 0)
                        ShotName_Text_Node['box'].setValue(33,   1)
                        ShotName_Text_Node['box'].setValue(900, 2)
                        ShotName_Text_Node['box'].setValue(33,   3)
                        ShotName_Text_Node['message'].setValue("""[lindex [split [lindex [split [ lindex [split [knob [topnode this.parent.input].file] .] 0] /] end ] _ ] 0]_[lindex [split [lindex [split [ lindex [split [knob [topnode this.parent.input].file] .] 0] /] end ] _ ] 1]_[lindex [split [lindex [split [ lindex [split [knob [topnode this.parent.input].file] .] 0] /] end ] _ ] 2]""")
                        BurninNode.end()
                        SwitchNode = nuke.nodes.Switch()
                        SwitchNode.setInput(0,TippettPath_SlateNode)
                        SwitchNode.setInput(1,BurninNode)
                        SwitchNode.setXYpos(BurninNode.xpos(),BurninNode.ypos()+90)
                        SwitchNode['which'].setAnimated()
                        SwitchNode['which'].setValueAt(1,JpgFirstFrame)
                        SwitchNode['which'].setValueAt(0,JpgFirstFrame-1)
                for x in nuke.allNodes():
                    x.setSelected(False)
                Final_HD_Reformat = nuke.nodes.Reformat()
                Final_HD_Reformat['name'].setValue("Final_HDReformat")
                Final_HD_Reformat['format'].setValue("HD_1080")
                Final_HD_Reformat['resize'].setValue("width")
                Final_HD_Reformat['black_outside'].setValue(True)
                Final_HD_Reformat['pbb'].setValue(True)
                Final_HD_Reformat.setXYpos(SwitchNode.xpos(),SwitchNode.ypos()+50)
                Final_HD_Reformat.setInput(0,SwitchNode)
                WriteNode.setInput(0,Final_HD_Reformat)
                WriteNode.setXYpos(SwitchNode.xpos(),SwitchNode.ypos()+120)
                WriteNode["file"].setValue(PreviewPath + RealPreviewFolder[0] +"." + Taraba +".png")

                
                try:
                    WriteNode['file_type'].setValue("png")
                    WriteNode['datatype'].setValue("16 Bit")
                except:
                    pass
                
                FrameRange = ("{}-{}".format(JpgFirstFrame-1,JpgLastFrame))
                print ("FrameRange = {}".format(FrameRange)) 
                nukescripts.renderdialog._gRenderDialogState.saveValue('frame_range', 'custom')
                nukescripts.renderdialog._gRenderDialogState.saveValue('frame_range_string', FrameRange)
            else:

                for x in nuke.allNodes():
                    x.setSelected(False)

            #    WriteNode.setSelected(True)
            #    nuke.toNode("Write1").setSelected(True)
                WriteNode = nuke.nodes.Write()
                WriteNode.setInput(0,MergeFinalNode)
                WriteNode.setXYpos(MergeFinalNode.xpos(),MergeFinalNode.ypos()+100)
                WriteNode["file"].setValue(PreviewPath + RealPreviewFolder[0] + "." + Taraba +".jpg")
                WriteNode['name'].setValue(ShotName + " WriteNode")
                try:
                    WriteNode['file_type'].setValue("jpeg")
                    WriteNode['_jpeg_quality'].setValue(1)
                except:
                    pass

    elif StudioName == "ImageEngine":
        try:
            nuke.delete(MergeTreesNode)
        except:
            pass
        if Cones_Check == True:
            MergeConesNode = nuke.nodes.Merge2()
        if Geo_Check == True:
            MergeGeoNode = nuke.nodes.Merge2()
        if Rig_Check == True:
            MergeRigNode = nuke.nodes.Merge2()
        if Lidar_Check:
            MergeLidarNode = nuke.nodes.Merge2()
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

        PreviewPath = OriginalPreviewPath + "Render"
        PreviewPath = PreviewPath.replace("\\","/")
        IEGeoName = IE_ShotID + "_wire_" + IEVersion
        IEGeoPath = PreviewPath  + "/" + "wire"        # + Version
        IELidarName = IE_ShotID + "_lidar_" + IEVersion
        IELidarPath = PreviewPath + "/" + "lidar"
        IEConesName = IE_ShotID + "_cone_" + IEVersion
        IEConesPath = PreviewPath  + "/" + "cone"

        if Cones_Check == True:
            MergeConesNode.setInput(1,CreateTree.ConesMergeNode)
            MergeConesNode.setXYpos(CreateTree.ConesMergeNode.xpos(),CreateTree.ConesMergeNode.ypos()+100)
            MergeConesNode['label'].setValue("ALL")
            BlurConesNode = nuke.nodes.Blur()
            BlurConesNode.setXYpos(MergeConesNode.xpos(),MergeConesNode.ypos()+80)
            BlurConesNode.setInput(0,MergeConesNode)
            BlurConesNode["size"].setValue(1.2)
            # IF this is an LD node type of shot
            if LDCheck == True and UV_LD_Status == "LD Node" :
                try:
                    for seq in nuke.getFileNameList(JPGPath):
                        Split = seq.split(" ")
                        Split.pop()
                        Split = "".join(Split)
                        if Split.endswith(".jpg"):
                            Read_JPG_Cones = nuke.createNode('Read')
                            Read_JPG_Cones.knob('file').fromUserText(JPGPath + seq)
                            JpgFirstFrame = Read_JPG_Cones['first'].value()
                            JpgLastFrame = Read_JPG_Cones['last'].value()
                            JPG_FORMAT = Read_JPG_Cones['format'].value()
                            PixelAspectJPG = Read_JPG_Cones.pixelAspect()
                            ReformatLDNode_Cones = nuke.nodes.Reformat()
                            ReformatLDNode_Cones['format'].setValue(JPG_FORMAT)
                            ReformatLDNode_Cones['black_outside'].setValue(True)
                            ReformatLDNode_Cones['pbb'].setValue(True)
                            ReformatLDNode_Cones['resize'].setValue("none")
                            ReformatLDNode_Cones.setXYpos(BlurConesNode.xpos(),BlurConesNode.ypos()+80)
                            ReformatLDNode_Cones.setInput(0,BlurConesNode)
                            
                except:
                    nuke.message('Cannot find JPG')
                    pass

                for LD in os.listdir(LDNodePath):
                    if "dist_".lower() in LD.lower():
                        Split,ext = os.path.splitext(LD)
                        SplitDist = Split.split("_")
                        for v in SplitDist:
                            if "v0" in v:
                                LastVersion = v
                                
                    try:
                        LastVersion
                    except NameError:
                        pass
                for LD in os.listdir(LDNodePath):
                    try:
                        if "dist_{}".format(LastVersion).lower() in LD.lower():
                            LDNodePath_ = LDNodePath + LD
                            LDNode_Cones = nuke.nodePaste(LDNodePath_)
                            LDNode_Cones['direction'].setValue("distort")
                            LDNode_Cones['name'].setValue(LDNode_Cones.name() + "_" + LastVersion)
                            LDNode_Cones.setInput(0,ReformatLDNode_Cones)
                            LDNode_Cones.setXYpos(ReformatLDNode_Cones.xpos(),ReformatLDNode_Cones.ypos()+80)
                            LDNode_Cones['disable'].setValue(True)
                            MergeFinalNode_Cones = nuke.nodes.Merge2()
                            MergeFinalNode_Cones.setXYpos(LDNode_Cones.xpos(),LDNode_Cones.ypos()+120)
                            MergeFinalNode_Cones.setInput(1,LDNode_Cones)
                            MergeFinalNode_Cones["name"].setValue("MergeFinal_Cones")
                            MergeFinalNode_Cones["label"].setValue("FINAL")
                            MergeFinalNode_Cones.setInput(0,Read_JPG_Cones)
                            Read_JPG_Cones.setXYpos(MergeFinalNode_Cones.xpos()+300,MergeFinalNode_Cones.ypos()-25)
                    except:
                            pass
                CONES_FORMAT = CreateTree.ConesReadNode['format'].actualValue()
                CONES_WIDTH = CONES_FORMAT.width()
                CONES_HEIGHT = CONES_FORMAT.height()
                JPG_HEIGHT = JPG_FORMAT.height()
                JPG_WIDTH = JPG_FORMAT.width()

                Image_Aspect = JPG_WIDTH / JPG_HEIGHT
                if Image_Aspect > 2.0:
                    Anamorphic = True

                print ("Anamorphic = {}".format(Anamorphic))
                print ("CONES_FORMAT = {}".format(CONES_FORMAT))
                print ("CONES_WIDTH = {}".format(CONES_WIDTH))
                print ("CONES_HEIGHT = {}".format(CONES_HEIGHT))
                print ("JPG_HEIGHT = {}".format(JPG_HEIGHT))
                print ("JPG_WIDTH = {}".format(JPG_WIDTH))
            #IF it is a UV MAP type of shot
            else:
                for uv in nuke.getFileNameList(UVDistortPath):
                    print (uv)
                    try:
                        if "redi" in uv.lower():
                            Read_RedistortEXR_Cones = nuke.createNode('Read')
                            Read_RedistortEXR_Cones.knob('file').fromUserText(UVDistortPath + uv)
                            Read_RedistortEXR_Cones['disable'].setValue(True)
            
                    except:
                        nuke.message("Missing Redist Map, name it 'redist' ")
                        pass

                STMapNode_Cones = nuke.nodes.STMap (uv="rgba")
                STMapNode_Cones.setInput(0,BlurConesNode)
                #    STMapNode_Cones.setInput(1,RedistNode)
                STMapNode_Cones.setXYpos(BlurConesNode.xpos(),BlurConesNode.ypos()+80)
                try:
                    STMapNode_Cones.setInput(1,Read_RedistortEXR_Cones)
                except:
                    pass
                try:
                    Read_RedistortEXR_Cones.setXYpos(STMapNode_Cones.xpos()+150,STMapNode_Cones.ypos()-25)
                except:
                    pass
                MergeFinalNode_Cones = nuke.nodes.Merge2()
                MergeFinalNode_Cones.setXYpos(STMapNode_Cones.xpos(),STMapNode_Cones.ypos()+120)
        #        MergeFinalNode_Cones.setInput(0,STMapNode_Cones)
                MergeFinalNode_Cones.setInput(1,STMapNode_Cones)
                MergeFinalNode_Cones["name"].setValue("Merge")
                MergeFinalNode_Cones["label"].setValue("FINAL")

                try:
                    for seq in nuke.getFileNameList(JPGPath):
                        Split = seq.split(" ")
                        Split.pop()
                        Split = "".join(Split)
                        if Split.endswith(".jpg"):
                            Read_JPG_Cones = nuke.createNode('Read')
                            try:
                                Read_JPG_Cones.knob('file').fromUserText(JPGPath + seq)
                                Read_JPG_Cones.setXYpos(MergeFinalNode_Cones.xpos()+300,MergeFinalNode_Cones.ypos()-25)
                                JpgFirstFrame = Read_JPG_Cones['first'].value()
                                JpgLastFrame = Read_JPG_Cones['last'].value()
                                JPG_FORMAT = Read_JPG_Cones['format'].value()
                                PixelAspectJPG = Read_JPG_Cones.pixelAspect()
                                MergeFinalNode_Cones.setInput(0,Read_JPG_Cones)
                            except:
                                pass 
                except:
                    nuke.message('Cannot find JPG')
                    pass
                
                CONES_FORMAT = CreateTree.ConesReadNode['format'].actualValue()
                CONES_WIDTH = CONES_FORMAT.width()
                CONES_HEIGHT = CONES_FORMAT.height()
                JPG_HEIGHT = JPG_FORMAT.height()
                JPG_WIDTH = JPG_FORMAT.width()

                Image_Aspect = JPG_WIDTH / JPG_HEIGHT
                if Image_Aspect > 2.0:
                    Anamorphic = True

                print ("Anamorphic = {}".format(Anamorphic))
                print ("CONES_FORMAT = {}".format(CONES_FORMAT))
                print ("CONES_WIDTH = {}".format(CONES_WIDTH))
                print ("CONES_HEIGHT = {}".format(CONES_HEIGHT))
                print ("JPG_HEIGHT = {}".format(JPG_HEIGHT))
                print ("JPG_WIDTH = {}".format(JPG_WIDTH))
                
                if Redist_Check == False and Undist_Check == False and LD_Check == False:
                    STMapNode_Cones['disable'].setValue(True)
                    print ("Undist and JPG are identical resolution")
                else:
                    print ("False equvalence")
            for x in nuke.allNodes():
                x.setSelected(False)

        #    WriteNodeCones.setSelected(True)
        #    nuke.toNode("Write1").setSelected(True)
            WriteNodeCones = nuke.nodes.Write()
            WriteNodeCones.setInput(0,MergeFinalNode_Cones)
            WriteNodeCones.setXYpos(MergeFinalNode_Cones.xpos(),MergeFinalNode_Cones.ypos()+100)
            if not os.path.exists(IEConesPath):
                original_umask = os.umask(0)
                os.makedirs(IEConesPath,mode=0o777  ) 
            WriteNodeCones["file"].setValue(IEConesPath + "/" + IEConesName + "." + Taraba +".jpg")
            WriteNodeCones['name'].setValue(ShotName + " WriteNodeCones")
            try:
                WriteNodeCones['file_type'].setValue("jpeg")
                WriteNodeCones['_jpeg_quality'].setValue(1)
            except:
                pass
        if Geo_Check == True and Rig_Check == True:
            MergeGeoNode.setInput(1,CreateTree.GeoMergeNode)
            MergeGeoNode.setXYpos(CreateTree.GeoMergeNode.xpos(),CreateTree.GeoMergeNode.ypos()+100)
            MergeGeoNode['label'].setValue("ALL")
            BlurGeoNode = nuke.nodes.Blur()
            BlurGeoNode.setXYpos(MergeGeoNode.xpos(),MergeGeoNode.ypos()+80)
            BlurGeoNode.setInput(0,MergeGeoNode)
            BlurGeoNode["size"].setValue(1.2)
            # IF this is an LD node type of shot
            if LDCheck == True and UV_LD_Status == "LD Node" :
                try:
                    for seq in nuke.getFileNameList(JPGPath):
                        Split = seq.split(" ")
                        Split.pop()
                        Split = "".join(Split)
                        if Split.endswith(".jpg"):
                            Read_JPG_Geo = nuke.createNode('Read')
                            Read_JPG_Geo.knob('file').fromUserText(JPGPath + seq)
                            JpgFirstFrame = Read_JPG_Geo['first'].value()
                            JpgLastFrame = Read_JPG_Geo['last'].value()
                            JPG_FORMAT = Read_JPG_Geo['format'].value()
                            PixelAspectJPG = Read_JPG_Geo.pixelAspect()
                            ReformatLDNode_Geo = nuke.nodes.Reformat()
                            ReformatLDNode_Geo['format'].setValue(JPG_FORMAT)
                            ReformatLDNode_Geo['black_outside'].setValue(True)
                            ReformatLDNode_Geo['pbb'].setValue(True)
                            ReformatLDNode_Geo['resize'].setValue("none")
                            ReformatLDNode_Geo.setXYpos(BlurGeoNode.xpos(),BlurGeoNode.ypos()+80)
                            ReformatLDNode_Geo.setInput(0,BlurGeoNode)
                            
                except:
                    nuke.message('Cannot find JPG')
                    pass

                for LD in os.listdir(LDNodePath):
                    if "dist_".lower() in LD.lower():
                        Split,ext = os.path.splitext(LD)
                        SplitDist = Split.split("_")
                        for v in SplitDist:
                            if "v0" in v:
                                LastVersion = v
                                
                    try:
                        LastVersion
                    except NameError:
                        pass
                for LD in os.listdir(LDNodePath):
                    try:
                        if "dist_{}".format(LastVersion).lower() in LD.lower():
                            LDNodePath_ = LDNodePath + LD
                            LDNode_Geo = nuke.nodePaste(LDNodePath_)
                            LDNode_Geo['direction'].setValue("distort")
                            LDNode_Geo['name'].setValue(LDNode_Geo.name() + "_" + LastVersion)
                            LDNode_Geo.setInput(0,ReformatLDNode_Geo)
                            LDNode_Geo.setXYpos(ReformatLDNode_Geo.xpos(),ReformatLDNode_Geo.ypos()+80)
                            LDNode_Geo['disable'].setValue(True)
                            MergeFinalNode_Geo = nuke.nodes.Merge2()
                            MergeFinalNode_Geo.setXYpos(LDNode_Geo.xpos(),LDNode_Geo.ypos()+120)
                            MergeFinalNode_Geo.setInput(1,LDNode_Geo)
                            MergeFinalNode_Geo["name"].setValue("MergeFinal_Geo")
                            MergeFinalNode_Geo["label"].setValue("FINAL")
                            MergeFinalNode_Geo.setInput(0,Read_JPG_Geo)
                            Read_JPG_Geo.setXYpos(MergeFinalNode_Geo.xpos()+300,MergeFinalNode_Geo.ypos()-25)
                    except:
                            pass
                CONES_FORMAT = CreateTree.ConesReadNode['format'].actualValue()
                CONES_WIDTH = CONES_FORMAT.width()
                CONES_HEIGHT = CONES_FORMAT.height()
                JPG_HEIGHT = JPG_FORMAT.height()
                JPG_WIDTH = JPG_FORMAT.width()

                Image_Aspect = JPG_WIDTH / JPG_HEIGHT
                if Image_Aspect > 2.0:
                    Anamorphic = True

                print ("Anamorphic = {}".format(Anamorphic))
                print ("CONES_FORMAT = {}".format(CONES_FORMAT))
                print ("CONES_WIDTH = {}".format(CONES_WIDTH))
                print ("CONES_HEIGHT = {}".format(CONES_HEIGHT))
                print ("JPG_HEIGHT = {}".format(JPG_HEIGHT))
                print ("JPG_WIDTH = {}".format(JPG_WIDTH))
            #IF it is a UV MAP type of shot
            else:
                for uv in nuke.getFileNameList(UVDistortPath):
                    print (uv)
                    try:
                        if "redi" in uv.lower():
                            Read_RedistortEXR_Geo = nuke.createNode('Read')
                            Read_RedistortEXR_Geo.knob('file').fromUserText(UVDistortPath + uv)
                            Read_RedistortEXR_Geo['disable'].setValue(True)
            
                    except:
                        nuke.message("Missing Redist Map, name it 'redist' ")
                        pass

                STMapNode_Geo = nuke.nodes.STMap (uv="rgba")
                STMapNode_Geo.setInput(0,BlurConesNode)
                #    STMapNode_Geo.setInput(1,RedistNode)
                STMapNode_Geo.setXYpos(BlurConesNode.xpos(),BlurConesNode.ypos()+80)
                try:
                    STMapNode_Geo.setInput(1,Read_RedistortEXR_Geo)
                except:
                    pass
                try:
                    Read_RedistortEXR_Geo.setXYpos(STMapNode_Geo.xpos()+150,STMapNode_Geo.ypos()-25)
                except:
                    pass
                MergeFinalNode_Geo = nuke.nodes.Merge2()
                MergeFinalNode_Geo.setXYpos(STMapNode_Geo.xpos(),STMapNode_Geo.ypos()+120)
        #        MergeFinalNode_Geo.setInput(0,STMapNode_Geo)
                MergeFinalNode_Geo.setInput(1,STMapNode_Geo)
                MergeFinalNode_Geo["name"].setValue("Merge")
                MergeFinalNode_Geo["label"].setValue("FINAL")

                try:
                    for seq in nuke.getFileNameList(JPGPath):
                        Split = seq.split(" ")
                        Split.pop()
                        Split = "".join(Split)
                        if Split.endswith(".jpg"):
                            Read_JPG_Geo = nuke.createNode('Read')
                            try:
                                Read_JPG_Geo.knob('file').fromUserText(JPGPath + seq)
                                Read_JPG_Geo.setXYpos(MergeFinalNode_Geo.xpos()+300,MergeFinalNode_Geo.ypos()-25)
                                JpgFirstFrame = Read_JPG_Geo['first'].value()
                                JpgLastFrame = Read_JPG_Geo['last'].value()
                                JPG_FORMAT = Read_JPG_Geo['format'].value()
                                PixelAspectJPG = Read_JPG_Geo.pixelAspect()
                                MergeFinalNode_Geo.setInput(0,Read_JPG_Geo)
                            except:
                                pass 
                except:
                    nuke.message('Cannot find JPG')
                    pass
                
                CONES_FORMAT = CreateTree.ConesReadNode['format'].actualValue()
                CONES_WIDTH = CONES_FORMAT.width()
                CONES_HEIGHT = CONES_FORMAT.height()
                JPG_HEIGHT = JPG_FORMAT.height()
                JPG_WIDTH = JPG_FORMAT.width()

                Image_Aspect = JPG_WIDTH / JPG_HEIGHT
                if Image_Aspect > 2.0:
                    Anamorphic = True

                print ("Anamorphic = {}".format(Anamorphic))
                print ("CONES_FORMAT = {}".format(CONES_FORMAT))
                print ("CONES_WIDTH = {}".format(CONES_WIDTH))
                print ("CONES_HEIGHT = {}".format(CONES_HEIGHT))
                print ("JPG_HEIGHT = {}".format(JPG_HEIGHT))
                print ("JPG_WIDTH = {}".format(JPG_WIDTH))
                
                if Redist_Check == False and Undist_Check == False and LD_Check == False:
                    STMapNode_Geo['disable'].setValue(True)
                    print ("Undist and JPG are identical resolution")
                else:
                    print ("False equvalence")
            for x in nuke.allNodes():
                x.setSelected(False)

        #    WriteNodeGeo.setSelected(True)
        #    nuke.toNode("Write1").setSelected(True)
            WriteNodeGeo = nuke.nodes.Write()
            WriteNodeGeo.setInput(0,MergeFinalNode_Geo)
            WriteNodeGeo.setXYpos(MergeFinalNode_Geo.xpos(),MergeFinalNode_Geo.ypos()+100)

            #WriteNodeGeo["file"].setValue(PreviewPath + RealPreviewFolder[0] + "." + Taraba +".jpg")
            
            
            
            if not os.path.exists(IEGeoPath):
                original_umask = os.umask(0)
                os.makedirs(IEGeoPath,mode=0o777  ) 
            WriteNodeGeo["file"].setValue(IEGeoPath + "/" + IEGeoName + "." + Taraba +".jpg")
            WriteNodeGeo['name'].setValue(ShotName + " WriteNodeGeo")
            try:
                WriteNodeGeo['file_type'].setValue("jpeg")
                WriteNodeGeo['_jpeg_quality'].setValue(1)
            except:
                pass
        
        if Geo_Check == False and Rig_Check == True:
            MergeRigNode.setInput(1,CreateTree.RigMergeNode)
            MergeRigNode.setXYpos(CreateTree.RigMergeNode.xpos(),CreateTree.RigMergeNode.ypos()+100)
            MergeRigNode['label'].setValue("ALL")
            BlurRigNode = nuke.nodes.Blur()
            BlurRigNode.setXYpos(MergeRigNode.xpos(),MergeRigNode.ypos()+80)
            BlurRigNode.setInput(0,MergeRigNode)
            BlurRigNode["size"].setValue(1.2)
            # IF this is an LD node type of shot
            if LDCheck == True and UV_LD_Status == "LD Node" :
                try:
                    for seq in nuke.getFileNameList(JPGPath):
                        Split = seq.split(" ")
                        Split.pop()
                        Split = "".join(Split)
                        if Split.endswith(".jpg"):
                            Read_JPG_Rig = nuke.createNode('Read')
                            Read_JPG_Rig.knob('file').fromUserText(JPGPath + seq)
                            JpgFirstFrame = Read_JPG_Rig['first'].value()
                            JpgLastFrame = Read_JPG_Rig['last'].value()
                            JPG_FORMAT = Read_JPG_Rig['format'].value()
                            PixelAspectJPG = Read_JPG_Rig.pixelAspect()
                            ReformatLDNode_Rig = nuke.nodes.Reformat()
                            ReformatLDNode_Rig['format'].setValue(JPG_FORMAT)
                            ReformatLDNode_Rig['black_outside'].setValue(True)
                            ReformatLDNode_Rig['pbb'].setValue(True)
                            ReformatLDNode_Rig['resize'].setValue("none")
                            ReformatLDNode_Rig.setXYpos(BlurRigNode.xpos(),BlurRigNode.ypos()+80)
                            ReformatLDNode_Rig.setInput(0,BlurRigNode)
                            
                except:
                    nuke.message('Cannot find JPG')
                    pass

                for LD in os.listdir(LDNodePath):
                    if "dist_".lower() in LD.lower():
                        Split,ext = os.path.splitext(LD)
                        SplitDist = Split.split("_")
                        for v in SplitDist:
                            if "v0" in v:
                                LastVersion = v
                                
                    try:
                        LastVersion
                    except NameError:
                        pass
                for LD in os.listdir(LDNodePath):
                    try:
                        if "dist_{}".format(LastVersion).lower() in LD.lower():
                            LDNodePath_ = LDNodePath + LD
                            LDNode_Rig = nuke.nodePaste(LDNodePath_)
                            LDNode_Rig['direction'].setValue("distort")
                            LDNode_Rig['name'].setValue(LDNode_Rig.name() + "_" + LastVersion)
                            LDNode_Rig.setInput(0,ReformatLDNode_Rig)
                            LDNode_Rig.setXYpos(ReformatLDNode_Rig.xpos(),ReformatLDNode_Rig.ypos()+80)
                            LDNode_Rig['disable'].setValue(True)
                            MergeFinalNode_Rig = nuke.nodes.Merge2()
                            MergeFinalNode_Rig.setXYpos(LDNode_Rig.xpos(),LDNode_Rig.ypos()+120)
                            MergeFinalNode_Rig.setInput(1,LDNode_Rig)
                            MergeFinalNode_Rig["name"].setValue("MergeFinal_Rig")
                            MergeFinalNode_Rig["label"].setValue("FINAL")
                            MergeFinalNode_Rig.setInput(0,Read_JPG_Rig)
                            Read_JPG_Rig.setXYpos(MergeFinalNode_Rig.xpos()+300,MergeFinalNode_Rig.ypos()-25)
                    except:
                            pass
                CONES_FORMAT = CreateTree.ConesReadNode['format'].actualValue()
                CONES_WIDTH = CONES_FORMAT.width()
                CONES_HEIGHT = CONES_FORMAT.height()
                JPG_HEIGHT = JPG_FORMAT.height()
                JPG_WIDTH = JPG_FORMAT.width()

                Image_Aspect = JPG_WIDTH / JPG_HEIGHT
                if Image_Aspect > 2.0:
                    Anamorphic = True

                print ("Anamorphic = {}".format(Anamorphic))
                print ("CONES_FORMAT = {}".format(CONES_FORMAT))
                print ("CONES_WIDTH = {}".format(CONES_WIDTH))
                print ("CONES_HEIGHT = {}".format(CONES_HEIGHT))
                print ("JPG_HEIGHT = {}".format(JPG_HEIGHT))
                print ("JPG_WIDTH = {}".format(JPG_WIDTH))
            #IF it is a UV MAP type of shot
            else:
                for uv in nuke.getFileNameList(UVDistortPath):
                    print (uv)
                    try:
                        if "redi" in uv.lower():
                            Read_RedistortEXR_Rig = nuke.createNode('Read')
                            Read_RedistortEXR_Rig.knob('file').fromUserText(UVDistortPath + uv)
                            Read_RedistortEXR_Rig['disable'].setValue(True)
            
                    except:
                        nuke.message("Missing Redist Map, name it 'redist' ")
                        pass

                STMapNode_Rig = nuke.nodes.STMap (uv="rgba")
                STMapNode_Rig.setInput(0,BlurConesNode)
                #    STMapNode_Rig.setInput(1,RedistNode)
                STMapNode_Rig.setXYpos(BlurConesNode.xpos(),BlurConesNode.ypos()+80)
                try:
                    STMapNode_Rig.setInput(1,Read_RedistortEXR_Rig)
                except:
                    pass
                try:
                    Read_RedistortEXR_Rig.setXYpos(STMapNode_Rig.xpos()+150,STMapNode_Rig.ypos()-25)
                except:
                    pass
                MergeFinalNode_Rig = nuke.nodes.Merge2()
                MergeFinalNode_Rig.setXYpos(STMapNode_Rig.xpos(),STMapNode_Rig.ypos()+120)
        #        MergeFinalNode_Rig.setInput(0,STMapNode_Rig)
                MergeFinalNode_Rig.setInput(1,STMapNode_Rig)
                MergeFinalNode_Rig["name"].setValue("Merge")
                MergeFinalNode_Rig["label"].setValue("FINAL")

                try:
                    for seq in nuke.getFileNameList(JPGPath):
                        Split = seq.split(" ")
                        Split.pop()
                        Split = "".join(Split)
                        if Split.endswith(".jpg"):
                            Read_JPG_Rig = nuke.createNode('Read')
                            try:
                                Read_JPG_Rig.knob('file').fromUserText(JPGPath + seq)
                                Read_JPG_Rig.setXYpos(MergeFinalNode_Rig.xpos()+300,MergeFinalNode_Rig.ypos()-25)
                                JpgFirstFrame = Read_JPG_Rig['first'].value()
                                JpgLastFrame = Read_JPG_Rig['last'].value()
                                JPG_FORMAT = Read_JPG_Rig['format'].value()
                                PixelAspectJPG = Read_JPG_Rig.pixelAspect()
                                MergeFinalNode_Rig.setInput(0,Read_JPG_Rig)
                            except:
                                pass 
                except:
                    nuke.message('Cannot find JPG')
                    pass
                
                CONES_FORMAT = CreateTree.ConesReadNode['format'].actualValue()
                CONES_WIDTH = CONES_FORMAT.width()
                CONES_HEIGHT = CONES_FORMAT.height()
                JPG_HEIGHT = JPG_FORMAT.height()
                JPG_WIDTH = JPG_FORMAT.width()

                Image_Aspect = JPG_WIDTH / JPG_HEIGHT
                if Image_Aspect > 2.0:
                    Anamorphic = True

                print ("Anamorphic = {}".format(Anamorphic))
                print ("CONES_FORMAT = {}".format(CONES_FORMAT))
                print ("CONES_WIDTH = {}".format(CONES_WIDTH))
                print ("CONES_HEIGHT = {}".format(CONES_HEIGHT))
                print ("JPG_HEIGHT = {}".format(JPG_HEIGHT))
                print ("JPG_WIDTH = {}".format(JPG_WIDTH))
                
                if Redist_Check == False and Undist_Check == False and LD_Check == False:
                    STMapNode_Rig['disable'].setValue(True)
                    print ("Undist and JPG are identical resolution")
                else:
                    print ("False equvalence")
            for x in nuke.allNodes():
                x.setSelected(False)

        #    WriteNodeRig.setSelected(True)
        #    nuke.toNode("Write1").setSelected(True)
            WriteNodeRig = nuke.nodes.Write()
            WriteNodeRig.setInput(0,MergeFinalNode_Rig)
            WriteNodeRig.setXYpos(MergeFinalNode_Rig.xpos(),MergeFinalNode_Rig.ypos()+100)
           
            if not os.path.exists(IEGeoPath):
                original_umask = os.umask(0)
                os.makedirs(IEGeoPath,mode=0o777  ) 
            WriteNodeRig["file"].setValue(IEGeoPath + "/" + IEGeoName + "." + Taraba +".jpg")
            WriteNodeRig['name'].setValue(ShotName + " WriteNodeRig")
            try:
                WriteNodeRig['file_type'].setValue("jpeg")
                WriteNodeRig['_jpeg_quality'].setValue(1)
            except:
                pass


        if Lidar_Check == True:
            MergeLidarNode.setInput(1,CreateTree.LidarMergeNode)
            MergeLidarNode.setXYpos(CreateTree.LidarMergeNode.xpos(),CreateTree.LidarMergeNode.ypos()+100)
            MergeLidarNode['label'].setValue("ALL")
            BlurLidarNode = nuke.nodes.Blur()
            BlurLidarNode.setXYpos(MergeLidarNode.xpos(),MergeLidarNode.ypos()+80)
            BlurLidarNode.setInput(0,MergeLidarNode)
            BlurLidarNode["size"].setValue(1.2)
            # IF this is an LD node type of shot
            if LDCheck == True and UV_LD_Status == "LD Node" :
                try:
                    for seq in nuke.getFileNameList(JPGPath):
                        Split = seq.split(" ")
                        Split.pop()
                        Split = "".join(Split)
                        if Split.endswith(".jpg"):
                            Read_JPG_Lidar = nuke.createNode('Read')
                            Read_JPG_Lidar.knob('file').fromUserText(JPGPath + seq)
                            JpgFirstFrame = Read_JPG_Lidar['first'].value()
                            JpgLastFrame = Read_JPG_Lidar['last'].value()
                            JPG_FORMAT = Read_JPG_Lidar['format'].value()
                            PixelAspectJPG = Read_JPG_Lidar.pixelAspect()
                            ReformatLDNode_Lidar = nuke.nodes.Reformat()
                            ReformatLDNode_Lidar['format'].setValue(JPG_FORMAT)
                            ReformatLDNode_Lidar['black_outside'].setValue(True)
                            ReformatLDNode_Lidar['pbb'].setValue(True)
                            ReformatLDNode_Lidar['resize'].setValue("none")
                            ReformatLDNode_Lidar.setXYpos(BlurLidarNode.xpos(),BlurLidarNode.ypos()+80)
                            ReformatLDNode_Lidar.setInput(0,BlurLidarNode)
                            
                except:
                    nuke.message('Cannot find JPG')
                    pass

                for LD in os.listdir(LDNodePath):
                    if "dist_".lower() in LD.lower():
                        Split,ext = os.path.splitext(LD)
                        SplitDist = Split.split("_")
                        for v in SplitDist:
                            if "v0" in v:
                                LastVersion = v
                                
                    try:
                        LastVersion
                    except NameError:
                        pass
                for LD in os.listdir(LDNodePath):
                    try:
                        if "dist_{}".format(LastVersion).lower() in LD.lower():
                            LDNodePath_ = LDNodePath + LD
                            LDNode_Lidar = nuke.nodePaste(LDNodePath_)
                            LDNode_Lidar['direction'].setValue("distort")
                            LDNode_Lidar['name'].setValue(LDNode_Lidar.name() + "_" + LastVersion)
                            LDNode_Lidar.setInput(0,ReformatLDNode_Lidar)
                            LDNode_Lidar.setXYpos(ReformatLDNode_Lidar.xpos(),ReformatLDNode_Lidar.ypos()+80)
                            MergeFinalNode_Lidar = nuke.nodes.Merge2()
                            MergeFinalNode_Lidar.setXYpos(LDNode_Lidar.xpos(),LDNode_Lidar.ypos()+120)
                            MergeFinalNode_Lidar.setInput(1,LDNode_Lidar)
                            MergeFinalNode_Lidar["name"].setValue("MergeFinal_Lidar")
                            MergeFinalNode_Lidar["label"].setValue("FINAL")
                            MergeFinalNode_Lidar.setInput(0,Read_JPG_Lidar)
                            Read_JPG_Lidar.setXYpos(MergeFinalNode_Lidar.xpos()+300,MergeFinalNode_Lidar.ypos()-25)
                    except:
                            pass
                CONES_FORMAT = CreateTree.ConesReadNode['format'].actualValue()
                CONES_WIDTH = CONES_FORMAT.width()
                CONES_HEIGHT = CONES_FORMAT.height()
                JPG_HEIGHT = JPG_FORMAT.height()
                JPG_WIDTH = JPG_FORMAT.width()

                Image_Aspect = JPG_WIDTH / JPG_HEIGHT
                if Image_Aspect > 2.0:
                    Anamorphic = True

                print ("Anamorphic = {}".format(Anamorphic))
                print ("CONES_FORMAT = {}".format(CONES_FORMAT))
                print ("CONES_WIDTH = {}".format(CONES_WIDTH))
                print ("CONES_HEIGHT = {}".format(CONES_HEIGHT))
                print ("JPG_HEIGHT = {}".format(JPG_HEIGHT))
                print ("JPG_WIDTH = {}".format(JPG_WIDTH))
            #IF it is a UV MAP type of shot
            else:
                for uv in nuke.getFileNameList(UVDistortPath):
                    print (uv)
                    try:
                        if "redi" in uv.lower():
                            Read_RedistortEXR_Lidar = nuke.createNode('Read')
                            Read_RedistortEXR_Lidar.knob('file').fromUserText(UVDistortPath + uv)
            
                    except:
                        nuke.message("Missing Redist Map, name it 'redist' ")
                        pass

                STMapNode_Lidar = nuke.nodes.STMap (uv="rgba")
                STMapNode_Lidar.setInput(0,BlurLidarNode)
                #    STMapNode_Lidar.setInput(1,RedistNode)
                STMapNode_Lidar.setXYpos(BlurLidarNode.xpos(),BlurLidarNode.ypos()+80)
                try:
                    STMapNode_Lidar.setInput(1,Read_RedistortEXR_Lidar)
                except:
                    pass
                try:
                    Read_RedistortEXR_Lidar.setXYpos(STMapNode_Lidar.xpos()+150,STMapNode_Lidar.ypos()-25)
                except:
                    pass
                MergeFinalNode_Lidar = nuke.nodes.Merge2()
                MergeFinalNode_Lidar.setXYpos(STMapNode_Lidar.xpos(),STMapNode_Lidar.ypos()+120)
        #        MergeFinalNode_Lidar.setInput(0,STMapNode_Lidar)
                MergeFinalNode_Lidar.setInput(1,STMapNode_Lidar)
                MergeFinalNode_Lidar["name"].setValue("Merge")
                MergeFinalNode_Lidar["label"].setValue("FINAL")

                try:
                    for seq in nuke.getFileNameList(JPGPath):
                        Split = seq.split(" ")
                        Split.pop()
                        Split = "".join(Split)
                        if Split.endswith(".jpg"):
                            Read_JPG_Lidar = nuke.createNode('Read')
                            try:
                                Read_JPG_Lidar.knob('file').fromUserText(JPGPath + seq)
                                Read_JPG_Lidar.setXYpos(MergeFinalNode_Lidar.xpos()+300,MergeFinalNode_Lidar.ypos()-25)
                                JpgFirstFrame = Read_JPG_Lidar['first'].value()
                                JpgLastFrame = Read_JPG_Lidar['last'].value()
                                JPG_FORMAT = Read_JPG_Lidar['format'].value()
                                PixelAspectJPG = Read_JPG_Lidar.pixelAspect()
                                MergeFinalNode_Lidar.setInput(0,Read_JPG_Lidar)
                            except:
                                pass 
                except:
                    nuke.message('Cannot find JPG')
                    pass
                
                CONES_FORMAT = CreateTree.ConesReadNode['format'].actualValue()
                CONES_WIDTH = CONES_FORMAT.width()
                CONES_HEIGHT = CONES_FORMAT.height()
                JPG_HEIGHT = JPG_FORMAT.height()
                JPG_WIDTH = JPG_FORMAT.width()

                Image_Aspect = JPG_WIDTH / JPG_HEIGHT
                if Image_Aspect > 2.0:
                    Anamorphic = True

                print ("Anamorphic = {}".format(Anamorphic))
                print ("CONES_FORMAT = {}".format(CONES_FORMAT))
                print ("CONES_WIDTH = {}".format(CONES_WIDTH))
                print ("CONES_HEIGHT = {}".format(CONES_HEIGHT))
                print ("JPG_HEIGHT = {}".format(JPG_HEIGHT))
                print ("JPG_WIDTH = {}".format(JPG_WIDTH))
                
                if Redist_Check == False and Undist_Check == False and LD_Check == False:
                    STMapNode_Lidar['disable'].setValue(True)
                    print ("Undist and JPG are identical resolution")
                else:
                    print ("False equvalence")
            for x in nuke.allNodes():
                x.setSelected(False)

        #    WriteNodeLidar.setSelected(True)
        #    nuke.toNode("Write1").setSelected(True)
            WriteNodeLidar = nuke.nodes.Write()
            WriteNodeLidar.setInput(0,MergeFinalNode_Lidar)
            WriteNodeLidar.setXYpos(MergeFinalNode_Lidar.xpos(),MergeFinalNode_Lidar.ypos()+100)
            
            if not os.path.exists(IELidarPath):
                original_umask = os.umask(0)
                os.makedirs(IELidarPath,mode=0o777  ) 
            WriteNodeLidar["file"].setValue(IELidarPath + "/" + IELidarName + "." + Taraba +".jpg")
            WriteNodeLidar['name'].setValue(ShotName + " WriteNodeLidar")
            try:
                WriteNodeLidar['file_type'].setValue("jpeg")
                WriteNodeLidar['_jpeg_quality'].setValue(1)
            except:
                pass
#    try:
    for transform in TransformNodes:
        transform.knob('scale').setValue(PixelAspectJPG,1)
        if PixelAspectJPG == 1:
            transform['disable'].setValue(True)
        else:
            if Cones_Check:
                transform['center'].setValue(CONES_WIDTH/2,0)
                transform['center'].setValue(CONES_HEIGHT/2,1)

            elif Geo_Check:
                transform['center'].setValue(GEO_WIDTH/2,0)
                transform['center'].setValue(GEO_HEIGHT/2,1)
            elif Rig_Check:
                transform['center'].setValue(RIG_WIDTH/2,0)
                transform['center'].setValue(RIG_HEIGHT/2,1)
    
#    except:
#        pass




    def CreateViewer(LastNode):
        Viewer = nuke.nodes.Viewer()
        Viewer.setInput(0, LastNode)
        Viewer.setXYpos(LastNode.xpos(), LastNode.ypos() + 70)
        nuke.show(Viewer)
        
    def CreateBackDropGeo():
        try:
            GeoNodes = [CreateTree.GeoReadNode,CreateTree.GeoTransformNode,CreateTree.GeoShuffleNode,CreateTree.GeoColorCorrectNode,CreateTree.GeoBlurNode,CreateTree.GeoErodeNode,CreateTree.GeoMergeNode]
            for w in nuke.allNodes():
                w.setSelected(False)
            for a in GeoNodes:
                a.setSelected(True)

            GeoBackDrop = nukescripts.autoBackdrop()
            GeoBackDrop.setName("GeoTree")
            GeoBackDrop['bdwidth'].setValue(GeoBackDrop['bdwidth'].value()*2.45)
            GeoBackDrop['bdheight'].setValue(GeoBackDrop['bdheight'].value()*1.10)
            GeoBackDrop['xpos'].setValue(CreateTree.GeoReadNode.xpos()-80)
            GeoBackDrop['tile_color'].setValue(3602658047)
            GeoBackDrop['label'].setValue("GEO")
            GeoBackDrop['note_font_size'].setValue(30)
            for w in nuke.allNodes():
                w.setSelected(False)
        except:
            pass

    def CreateBackDropLidar():
        try:
            LidarNodes = [CreateTree.LidarReadNode,CreateTree.LidarTransformNode,CreateTree.LidarShuffleNode,CreateTree.LidarColorCorrectNode,CreateTree.LidarBlurNode,CreateTree.LidarErodeNode,CreateTree.LidarMergeNode]
            for w in nuke.allNodes():
                w.setSelected(False)
            for a in LidarNodes:
                a.setSelected(True)

            LidarBackDrop = nukescripts.autoBackdrop()
            LidarBackDrop.setName("LidarTree")
            LidarBackDrop['bdwidth'].setValue(LidarBackDrop['bdwidth'].value()*2.45)
            LidarBackDrop['bdheight'].setValue(LidarBackDrop['bdheight'].value()*1.10)
            LidarBackDrop['xpos'].setValue(CreateTree.LidarReadNode.xpos()-80)
            LidarBackDrop['tile_color'].setValue(3602658047)                            #Yellow
            LidarBackDrop['label'].setValue("Lidar")
            LidarBackDrop['note_font_size'].setValue(30)
            for w in nuke.allNodes():
                w.setSelected(False)
        except:
            pass

    def CreateBackDropLidar1():
        print("LIDAR1 BACKDROP")
        try:
            Lidar1Nodes = [CreateTree.Lidar1ReadNode,CreateTree.Lidar1TransformNode,CreateTree.Lidar1ShuffleNode,CreateTree.Lidar1ColorCorrectNode,CreateTree.Lidar1BlurNode,CreateTree.Lidar1ErodeNode,CreateTree.Lidar1MergeNode]
            for w in nuke.allNodes():
                w.setSelected(False)
            for a in Lidar1Nodes:
                a.setSelected(True)

            Lidar1BackDrop = nukescripts.autoBackdrop()
            Lidar1BackDrop.setName("Lidar1Tree")
            Lidar1BackDrop['bdwidth'].setValue(Lidar1BackDrop['bdwidth'].value()*2.45)
            Lidar1BackDrop['bdheight'].setValue(Lidar1BackDrop['bdheight'].value()*1.10)
            Lidar1BackDrop['xpos'].setValue(CreateTree.Lidar1ReadNode.xpos()-80)
            Lidar1BackDrop['tile_color'].setValue(966383359)                           #Blue
            Lidar1BackDrop['label'].setValue("Lidar1")
            Lidar1BackDrop['note_font_size'].setValue(30)
            for w in nuke.allNodes():
                w.setSelected(False)
        except:
            print("ERRA1")
            pass
    
    def CreateBackDropLidar2():
        print("LIDAR2 BACKDROP")
        try:
            Lidar2Nodes = [CreateTree.Lidar2ReadNode,CreateTree.Lidar2TransformNode,CreateTree.Lidar2ShuffleNode,CreateTree.Lidar2ColorCorrectNode,CreateTree.Lidar2BlurNode,CreateTree.Lidar2ErodeNode,CreateTree.Lidar2MergeNode]
            for w in nuke.allNodes():
                w.setSelected(False)
            for a in Lidar2Nodes:
                a.setSelected(True)

            Lidar2BackDrop = nukescripts.autoBackdrop()
            Lidar2BackDrop.setName("Lidar2Tree")
            Lidar2BackDrop['bdwidth'].setValue(Lidar2BackDrop['bdwidth'].value()*2.45)
            Lidar2BackDrop['bdheight'].setValue(Lidar2BackDrop['bdheight'].value()*1.10)
            Lidar2BackDrop['xpos'].setValue(CreateTree.Lidar2ReadNode.xpos()-80)
            Lidar2BackDrop['tile_color'].setValue(3599315455)                           #Orange
            Lidar2BackDrop['label'].setValue("Lidar2")
            Lidar2BackDrop['note_font_size'].setValue(30)
            for w in nuke.allNodes():
                w.setSelected(False)
        except:
            print("ERRA2")
            pass



    def CreateBackDropCones():
        try:
            ConesNodes = [CreateTree.ConesReadNode,CreateTree.ConesTransformNode,CreateTree.ConesShuffleNode,CreateTree.ConesColorCorrectNode,CreateTree.ConesBlurNode,CreateTree.ConesErodeNode,CreateTree.ConesMergeNode]
            for w in nuke.allNodes():
                w.setSelected(False)
            for a in ConesNodes:
                a.setSelected(True)

            ConesBackDrop = nukescripts.autoBackdrop()
            ConesBackDrop.setName("ConesTree")
            ConesBackDrop['bdwidth'].setValue(ConesBackDrop['bdwidth'].value()*2.45)
            ConesBackDrop['bdheight'].setValue(ConesBackDrop['bdheight'].value()*1.10)
            ConesBackDrop['xpos'].setValue(CreateTree.ConesReadNode.xpos()-80)
            ConesBackDrop['tile_color'].setValue(2821117695)
            ConesBackDrop['label'].setValue("CONES")
            ConesBackDrop['note_font_size'].setValue(30)
            for w in nuke.allNodes():
                w.setSelected(False)
        except:
            pass
    def CreateBackDropRig():
        try:
            RigNodes = [CreateTree.RigReadNode,CreateTree.RigTransformNode,CreateTree.RigShuffleNode,CreateTree.RigColorCorrectNode,CreateTree.RigBlurNode,CreateTree.RigErodeNode,CreateTree.RigMergeNode]
            for w in nuke.allNodes():
                w.setSelected(False)
            for a in RigNodes:
                a.setSelected(True)

            RigBackDrop = nukescripts.autoBackdrop()
            RigBackDrop.setName("RigTree")
            RigBackDrop['bdwidth'].setValue(RigBackDrop['bdwidth'].value()*2.45)
            RigBackDrop['bdheight'].setValue(RigBackDrop['bdheight'].value()*1.10)
            RigBackDrop['xpos'].setValue(CreateTree.RigReadNode.xpos()-80)
            RigBackDrop['tile_color'].setValue(12310271)
            RigBackDrop['label'].setValue("RIG")
            RigBackDrop['note_font_size'].setValue(30)
            for w in nuke.allNodes():
                w.setSelected(False)
        except:
            pass
    def CreateBackDropRig1():
        try:
            Rig1Nodes = [CreateTree.Rig1ReadNode,CreateTree.Rig1TransformNode,CreateTree.Rig1ShuffleNode,CreateTree.Rig1ColorCorrectNode,CreateTree.Rig1BlurNode,CreateTree.Rig1ErodeNode,CreateTree.Rig1MergeNode]
            for w in nuke.allNodes():
                w.setSelected(False)
            for a in Rig1Nodes:
                a.setSelected(True)

            Rig1BackDrop = nukescripts.autoBackdrop()
            Rig1BackDrop.setName("Rig1Tree")
            Rig1BackDrop['bdwidth'].setValue(Rig1BackDrop['bdwidth'].value()*2.45)
            Rig1BackDrop['bdheight'].setValue(Rig1BackDrop['bdheight'].value()*1.10)
            Rig1BackDrop['xpos'].setValue(CreateTree.Rig1ReadNode.xpos()-80)
            Rig1BackDrop['tile_color'].setValue(173342719)
            Rig1BackDrop['label'].setValue("Rig1")
            Rig1BackDrop['note_font_size'].setValue(30)
            for w in nuke.allNodes():
                w.setSelected(False)
        except:
            pass
    def CreateBackDropRig2():
        try:
            Rig2Nodes = [CreateTree.Rig2ReadNode,CreateTree.Rig2TransformNode,CreateTree.Rig2ShuffleNode,CreateTree.Rig2ColorCorrectNode,CreateTree.Rig2BlurNode,CreateTree.Rig2ErodeNode,CreateTree.Rig2MergeNode]
            for w in nuke.allNodes():
                w.setSelected(False)
            for a in Rig2Nodes:
                a.setSelected(True)

            Rig2BackDrop = nukescripts.autoBackdrop()
            Rig2BackDrop.setName("Rig2Tree")
            Rig2BackDrop['bdwidth'].setValue(Rig2BackDrop['bdwidth'].value()*2.45)
            Rig2BackDrop['bdheight'].setValue(Rig2BackDrop['bdheight'].value()*1.10)
            Rig2BackDrop['xpos'].setValue(CreateTree.Rig2ReadNode.xpos()-80)
            Rig2BackDrop['tile_color'].setValue(436147455)
            Rig2BackDrop['label'].setValue("Rig2")
            Rig2BackDrop['note_font_size'].setValue(30)
            for w in nuke.allNodes():
                w.setSelected(False)
        except:
            pass  
    def CreateBackDropRig3():
        try:
            Rig3Nodes = [CreateTree.Rig3ReadNode,CreateTree.Rig3TransformNode,CreateTree.Rig3ShuffleNode,CreateTree.Rig3ColorCorrectNode,CreateTree.Rig3BlurNode,CreateTree.Rig3ErodeNode,CreateTree.Rig3MergeNode]
            for w in nuke.allNodes():
                w.setSelected(False)
            for a in Rig3Nodes:
                a.setSelected(True)

            Rig3BackDrop = nukescripts.autoBackdrop()
            Rig3BackDrop.setName("Rig3Tree")
            Rig3BackDrop['bdwidth'].setValue(Rig3BackDrop['bdwidth'].value()*2.45)
            Rig3BackDrop['bdheight'].setValue(Rig3BackDrop['bdheight'].value()*1.10)
            Rig3BackDrop['xpos'].setValue(CreateTree.Rig3ReadNode.xpos()-80)
            Rig3BackDrop['tile_color'].setValue(4282993919)
            Rig3BackDrop['label'].setValue("Rig3")
            Rig3BackDrop['note_font_size'].setValue(30)
            for w in nuke.allNodes():
                w.setSelected(False)
        except:
            pass  
    def CreateBackDropRig4():
        try:
            Rig4Nodes = [CreateTree.Rig4ReadNode,CreateTree.Rig4TransformNode,CreateTree.Rig4ShuffleNode,CreateTree.Rig4ColorCorrectNode,CreateTree.Rig4BlurNode,CreateTree.Rig4ErodeNode,CreateTree.Rig4MergeNode]
            for w in nuke.allNodes():
                w.setSelected(False)
            for a in Rig4Nodes:
                a.setSelected(True)

            Rig4BackDrop = nukescripts.autoBackdrop()
            Rig4BackDrop.setName("Rig4Tree")
            Rig4BackDrop['bdwidth'].setValue(Rig4BackDrop['bdwidth'].value()*2.45)
            Rig4BackDrop['bdheight'].setValue(Rig4BackDrop['bdheight'].value()*1.10)
            Rig4BackDrop['xpos'].setValue(CreateTree.Rig4ReadNode.xpos()-80)
            Rig4BackDrop['tile_color'].setValue(4278196735)
            Rig4BackDrop['label'].setValue("Rig4")
            Rig4BackDrop['note_font_size'].setValue(30)
            for w in nuke.allNodes():
                w.setSelected(False)
        except:
            pass
    def CreateBackDropRig5():
        try:
            Rig5Nodes = [CreateTree.Rig5ReadNode,CreateTree.Rig5TransformNode,CreateTree.Rig5ShuffleNode,CreateTree.Rig5ColorCorrectNode,CreateTree.Rig5BlurNode,CreateTree.Rig5ErodeNode,CreateTree.Rig5MergeNode]
            for w in nuke.allNodes():
                w.setSelected(False)
            for a in Rig5Nodes:
                a.setSelected(True)

            Rig5BackDrop = nukescripts.autoBackdrop()
            Rig5BackDrop.setName("Rig5Tree")
            Rig5BackDrop['bdwidth'].setValue(Rig5BackDrop['bdwidth'].value()*2.45)
            Rig5BackDrop['bdheight'].setValue(Rig5BackDrop['bdheight'].value()*1.10)
            Rig5BackDrop['xpos'].setValue(CreateTree.Rig5ReadNode.xpos()-80)
            Rig5BackDrop['tile_color'].setValue(4285799679)
            Rig5BackDrop['label'].setValue("Rig5")
            Rig5BackDrop['note_font_size'].setValue(30)
            for w in nuke.allNodes():
                w.setSelected(False)
        except:
            pass      
    if Cones_Check:
        CreateBackDropCones()
    if Geo_Check:
        CreateBackDropGeo()
    if Lidar_Check:
        print("LIDAR CHECK PASSED")
        CreateBackDropLidar()

    print ("Lidar1_Check: {}".format(Lidar1_Check))
    print ("Lidar2_Check: {}".format(Lidar2_Check))
    if Lidar1_Check:
        print("LIDAR1 CHECK PASSED")
        CreateBackDropLidar1()
    if Lidar2_Check:
        print("LIDAR2 CHECK PASSED")
        CreateBackDropLidar2()
    if Rig_Check:
        CreateBackDropRig()
    if Rig1_Check:
        CreateBackDropRig1()
    if Rig2_Check:
        CreateBackDropRig2()
    if Rig3_Check:
        CreateBackDropRig3()
    if Rig4_Check:
        CreateBackDropRig4()
    if Rig5_Check:
        CreateBackDropRig5()
    try:
        if StudioName == "Pixomondo":
            CreateViewer(WriteWireFrameEXRNode)
        elif StudioName == "ImageEngine":
            CreateViewer(WriteNodeCones)
        else:
            CreateViewer(WriteNode)
    except:
        pass

    nuke.scriptSaveAs(SaveNukePreviewPath +"{}".format(ShotName) +"_preview_" + Version + ".nk", overwrite=1)
    nuke.selectAll()
    nuke.zoomToFitSelected()
    for node in nuke.selectedNodes():
        node.knob("selected").setValue(False)
    try:
        nuke.show(WriteNode)
    except:
        pass
    nuke.clearDiskCache
    nuke.clearRAMCache

    if StudioName=="Tippett":
        SG_Lens = nuke.getInput("SG Lens in mm", )
        if SG_Lens:
            if "mm" in SG_Lens:
                SG_Lens = SG_Lens.replace("mm","")

        if SG_Lens:
            TippettPath_SlateNode['sg_lens'].setValue(SG_Lens + "mm")
        else:
            TippettPath_SlateNode['sg_lens'].setValue(SG_Lens)

def NukeFiles_Checker(ShotName, ThreeD_comp_Path,render_Path,jpg_Path,Version,PIS_Status,UV_LD_Status):
    global Redist_Check
    global Undist_Check
    global LD_Check
    print ("Version = {}".format(Version))
    print ("PIS_Status = {}".format(PIS_Status))
    UVDistortPath=render_Path + "\\uvmap\\"
    UVContent = os.listdir(UVDistortPath)
    Redist_Check = False
    Undist_Check = False
    LD_Check = False
    if not UVContent:
        print ("No Redist or Undist")
        Redist_Check = False
        Undist_Check = False
        print ("Redist_Check = {}".format(Redist_Check))
    elif UVContent:
        for uv in UVContent:
            if "redi" in uv:
                Redist_Check = True
                print ("Redist_Check = {}".format(Redist_Check))
            elif "undi" in uv:
                Undist_Check = True
                print ("Undist_Check = {}".format(Undist_Check))

    LDNodePath = ThreeD_comp_Path +  "\\nuke\\"

    if not os.path.exists(LDNodePath):
            original_umask = os.umask(0)
            os.makedirs(LDNodePath,mode=0o777  ) 
#    try:
    for LD in os.listdir(LDNodePath):
        if "dist_".lower() in LD.lower():
            Split,ext = os.path.splitext(LD)
            SplitDist = Split.split("_")
            for v in SplitDist:
                if "v0" in v:
                    LastVersion = v
                    
        try:
            LastVersion
        except NameError:
            LastVersion = "v001"
            pass
     
    for LD in os.listdir(LDNodePath):
        if "dist_{}".format(LastVersion).lower() in LD.lower():
            LD_Check = True
            print ("LD_Check is = {}".format(LD_Check))
            if UV_LD_Status == "LD Node":
                Nuke_Preview(ShotName, ThreeD_comp_Path,render_Path,jpg_Path,Version,PIS_Status,UV_LD_Status)
                break

    else:
        if Redist_Check == True and Undist_Check == True:
            print ("UV Maps Found")
            if UV_LD_Status == "UV Map":
                Nuke_Preview(ShotName, ThreeD_comp_Path,render_Path,jpg_Path,Version,PIS_Status,UV_LD_Status)
            elif UV_LD_Status == "LD Node" and LD_Check == False:
                nuke.message("Missing LD Node in 'nuke' folder. Should be named 'dist_v001'. Try UV Map instead ? ")
            elif UV_LD_Status == "LD Node" and LD_Check == True:
                print ("UV Maps AND LD Node Found")
                Nuke_Preview(ShotName, ThreeD_comp_Path,render_Path,jpg_Path,Version,PIS_Status,UV_LD_Status)

        elif Redist_Check == False and Undist_Check == False and LD_Check == False:
            nuke.message("Missing LD Node or UV Maps")
            print ("Missing LD Node or UV Maps")
           # Nuke_Preview(ShotName, ThreeD_comp_Path,render_Path,jpg_Path,Version,PIS_Status,UV_LD_Status)
        else:
            nuke.message("Missing Undist/Redist. Try LD Node instead ?")
            print ("Missing Undist/Redist. Try LD Node instead ?")
#    except:
#    if Redist_Check == True and Undist_Check == True:
#            print ("Redist Found")
#            Nuke_Preview(ShotName, ThreeD_comp_Path,render_Path,jpg_Path,Version)
#    else:
#        nuke.message("Missing Undist/Redist EXCEPTION")
#        print ("Missing Undist/Redist EXCEPTION")

#NukeFiles_Checker(ShotName, ThreeD_comp_Path,render_Path,jpg_Path,Version)

#Nuke_Preview(ShotName, ThreeD_comp_Path,render_Path,jpg_Path,Version)



#ShotName = "Shadowbone2_207_207-039-5900_MP1_v001"
#ThreeD_comp_Path = r"\\fs3\TPN\CraftyApes\Origami\3d_comp\Shadowbone2_207_207-039-5900_MP1_v001"
#render_Path = r"\\fs3\TPN\CraftyApes\Origami\render\Shadowbone2_207_207-039-5900_MP1_v001"
#jpg_Path = r"\\fs3\TPN\CraftyApes\Origami\input\CRA_Vertigo_2022.11.16\Shadowbone2_207_207-039-5900_MP1_v001\jpg"
#Version = "v001"

#NukeFiles_Checker(ShotName, ThreeD_comp_Path,render_Path,jpg_Path,Version)