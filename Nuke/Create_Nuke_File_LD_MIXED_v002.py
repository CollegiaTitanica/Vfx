import os,webbrowser,nuke,nukescripts


def Create_LD_Node(ShotName, ThreeD_comp_Path,render_Path,jpg_Path,Version):
    
    #Search for LD Node
    LDNodePath = ThreeD_comp_Path +  "\\nuke\\"
    print (os.listdir(LDNodePath))
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
                LDNodeJPG = nuke.nodePaste(LDNodePath)
                LDNodeJPG['direction'].setValue("distort")
                LDNodeJPG['name'].setValue(LDNodeJPG.name() + "_" + LastVersion)
                
                #   LDNodeJPG.setXYpos(BlackOutsideNode.xpos(),BlackOutsideNode.ypos()+60)
                #   LDNodeJPG.setInput(0,BlackOutsideNode)
                LDNodeUndist = nuke.nodePaste(LDNodePath)
                LDNodeUndist['direction'].setValue("undistort")
                #   LDNodeUndist.setXYpos(ReformatNode.xpos(),ReformatNode.ypos()+60)
                break
        except:
                nuke.message("Missing LD Node")
            #    pass

    ProjectPath = render_Path.split("\\")[:-2]
    ProjectPath = "/".join(ProjectPath)
    ProjectName = ProjectPath[-1]
    StudioName = ProjectPath[-2]
    print ("ProjectPath = {}".format(ProjectPath))
    JPGPath=jpg_Path + "\\"
    JPGPath=JPGPath.replace("\\","/")
    print ("JPGPath = {}".format(JPGPath))                  
    for seq in nuke.getFileNameList(JPGPath):
        Split = seq.split(" ")
        Split.pop()
        Split = "".join(Split)
        if Split.endswith(".jpg"):
            Read_JPG = nuke.createNode('Read')
            try:
                Read_JPG.knob('file').fromUserText(JPGPath + seq)
            except:
                pass
    JPG_FORMAT = Read_JPG['format'].value()
    print ("JPG_FORMAT = {}".format(JPG_FORMAT))            
    OriginalUndistPath=render_Path + "\\undist\\"
    OriginalUndistPath=OriginalUndistPath.replace("\\","/")
    BlackOutsideNode = nuke.createNode("BlackOutside")
    BlackOutsideNode.setXYpos(Read_JPG.xpos(),Read_JPG.ypos()+120)
    try:
        LDNodeUndist.setXYpos(BlackOutsideNode.xpos(),BlackOutsideNode.ypos()+60)
        LDNodeUndist.setInput(0,BlackOutsideNode)
    except:
        nuke.message("Missing LD Node")
    
    UndistFolder=os.listdir(OriginalUndistPath)
    for folders in UndistFolder:
        SplitFolderName= folders.split("_")
        Reversed_SplitFolderName = reversed(SplitFolderName)
        print ("OriginalSplitFolderName = {}".format(SplitFolderName))
        LastSLOG = SplitFolderName[-1]
    #    UndistFolderName="_".join(SplitFolderName)
        if LastSLOG=="undist" or LastSLOG =="undistorted":
            for index,v in enumerate(Reversed_SplitFolderName):
                if LastSLOG=="undist" or LastSLOG =="undistorted":
                    if "v00" in v:
                        (SplitFolderName[-index-1]) = Version
                        break

                UndistFolderName="_".join(SplitFolderName)
            print ("UndistFolderName         = {}".format(UndistFolderName))
            print ("LastSLOG         = {}".format(LastSLOG))
            print ("SplitFolderName         = {}".format(SplitFolderName))

    #print ("OriginalUndistPath = {}".format(OriginalUndistPath))
    #print ("UndistPath = {}".format(UndistFolderName))
    try:
        for seq in nuke.getFileNameList(OriginalUndistPath + UndistFolderName): 
            print ("seq = {}".format(seq))
            try:
                Split = seq.split(" ")
                Split.pop()
                Split = "".join(Split)
                if Split.endswith(".jpg"):
                    Read_Undist = nuke.createNode('Read')
                    Read_Undist.knob('file').fromUserText(OriginalUndistPath + UndistFolderName + "/"+ seq)
            except:
                pass
    except UnboundLocalError:
        nuke.message("""Missing Undist! Undist Folder should end with '_undist' """)
        #nuke.scriptExit()
    Read_Undist.setXYpos(Read_JPG.xpos()-170,Read_JPG.ypos())
    ReformatNode = nuke.createNode("Reformat")
    ReformatNode['resize'].setValue("none")
    ReformatNode['format'].setValue(JPG_FORMAT)
    ReformatNode['pbb'].setValue(True)
    ReformatNode.setXYpos(Read_Undist.xpos(),Read_Undist.ypos()+120)
    LDNodeJPG.setInput(0,ReformatNode)
    LDNodeJPG.setXYpos(ReformatNode.xpos(),ReformatNode.ypos()+80)

    #Read_Undist = nuke.toNode("Read2")
    Read_UndistFormat = Read_Undist.format()
    Read_UndistFormat.setPixelAspect(3.0)
    Read_UndistFormat.setName("AAAA")
    Read_UndistFormat.setHeight(3404)
    

    JPG = Read_JPG
    JPGFormat = JPG['format'].value()
    JPGPixelAspect = JPG.pixelAspect()
    print ("JPGFormat = {}".format(JPGFormat))
    print ("JPGPixelAspect = {}".format(JPGPixelAspect))

    Undist = Read_Undist
    UndistFormat = Undist['format'].value()
    UndistPixelAspect = Undist.pixelAspect()
    print ("UndistFormat = {}".format(UndistFormat))
    print ("UndistPixelAspect = {}".format(UndistPixelAspect))

    if UndistPixelAspect != JPGPixelAspect:
        UndistFormat.setPixelAspect(JPGPixelAspect)

    else:
        print("Pixel Aspects are the same")

    newUndistPixelAspect= UndistFormat.pixelAspect()
    print ("newUndistPixelAspect = {}".format(newUndistPixelAspect))
    
    UNDIST_FORMAT = Read_Undist['format'].value()
    ReformatNodeUndist = nuke.nodes.Reformat()
    ReformatNodeUndist['resize'].setValue("none")
    ReformatNodeUndist.setInput(0, LDNodeUndist)
    ReformatNodeUndist["format"].setValue(UNDIST_FORMAT)
    ReformatNodeUndist['pbb'].setValue(True)
    ReformatNodeUndist.setXYpos(LDNodeUndist.xpos(),LDNodeUndist.ypos()+60)
    

    SaveNukePath = "{}".format(ThreeD_comp_Path) + "\\" + "nuke" + "\\" + "LD\\"
    print ("SaveNukePath = {}".format(SaveNukePath))
    if not os.path.exists(SaveNukePath):
        original_umask = os.umask(0)
        os.makedirs(SaveNukePath,mode=0o777  ) 
    
#    nuke.scriptSaveAs(SaveNukePath +"{}".format(ShotName) +"_distort_" + Version + ".nk", overwrite=1)    
    try:
        Viewer = nuke.nodes.Viewer()
        Viewer.setXYpos(ReformatNodeUndist.xpos()-70, ReformatNodeUndist.ypos()+40)
        Viewer.setInput(0, ReformatNodeUndist)
        Viewer.setInput(1, Read_Undist)
        Viewer.setInput(2, LDNodeJPG)
        Viewer.setInput(3, Read_JPG)
        
        nuke.show(Viewer)
    except:
        pass

    UNDIST_BACKDROP = [Read_JPG,BlackOutsideNode,LDNodeUndist,ReformatNodeUndist]
    REDIST_BACKDROP = [Read_Undist,ReformatNode,LDNodeJPG]
    print (UNDIST_BACKDROP)
    print (REDIST_BACKDROP)

    for w in nuke.allNodes():
        w.setSelected(False)
    for a in UNDIST_BACKDROP:
        a.setSelected(True)

    BackDropUndist = nukescripts.autoBackdrop()
    BackDropUndist.setName("Undist")
    BackDropUndist['bdwidth'].setValue(BackDropUndist['bdwidth'].value()*1.05)
    BackDropUndist['bdheight'].setValue(BackDropUndist['bdheight'].value()*1.18)
    BackDropUndist['tile_color'].setValue(1225392639)
    for w in nuke.allNodes():
        w.setSelected(False)
    for b in REDIST_BACKDROP:
        b.setSelected(True)
    BackDropRedist = nukescripts.autoBackdrop()
    BackDropRedist.setName("Redist")
    BackDropRedist['bdwidth'].setValue(BackDropRedist['bdwidth'].value()*1.05)
    BackDropRedist['bdheight'].setValue(BackDropRedist['bdheight'].value()*1.18)
    BackDropRedist['tile_color'].setValue(564018431)

    for a in nuke.allNodes():
        a.setSelected(True)
    BackDrop = nukescripts.autoBackdrop()
    BackDrop.setName("Apply_Remove_Distortion")
    BackDrop['bdwidth'].setValue(BackDrop['bdwidth'].value()*1.05)
    BackDrop['bdheight'].setValue(BackDrop['bdheight'].value()*1.18)
    BackDrop['tile_color'].setValue(1214680319)

    nuke.selectAll()
    nuke.zoomToFitSelected()
    for node in nuke.selectedNodes():
        node.knob("selected").setValue(False)
    
    if StudioName == "ILP":
        VertVersion = []

        for n in Version:
            if "v".lower() not in n:
                VertVersion.append(n)
        Version = "".join(VertVersion)
        nuke.scriptSaveAs(SaveNukePath +"{}".format(ShotName) +"_lensDistort_" + "vert_" + Version + ".nk", overwrite=1)
    else:
        nuke.scriptSaveAs(SaveNukePath +"{}".format(ShotName) +"_distort_" + Version + ".nk", overwrite=1) 
def Create_Nuke_File(ShotName, ThreeD_comp_Path,render_Path,jpg_Path,Version):
    
    ProjectPath = render_Path.split("\\")[:-2]
    ProjectPath = "/".join(ProjectPath)
    print ("ProjectPath = {}".format(ProjectPath))
    ProjectName = ProjectPath[-1]
    StudioName = ProjectPath[-2]
    JPGPath=jpg_Path + "\\"
    JPGPath=JPGPath.replace("\\","/")
    print ("JPGPath = {}".format(JPGPath))                  
    for seq in nuke.getFileNameList(JPGPath):
        Split = seq.split(" ")
        Split.pop()
        Split = "".join(Split)
        if Split.endswith(".jpg"):
            Read_JPG = nuke.createNode('Read')
            Read_JPG.knob('file').fromUserText(JPGPath + seq)
    BlackOutsideNode = nuke.createNode("BlackOutside")
    BlackOutsideNode.setXYpos(Read_JPG.xpos(),Read_JPG.ypos()+90)
    STNodeJPG = nuke.createNode('STMap')
    STNodeJPG['uv'].setValue("rgba")
    STNodeJPG.setXYpos(Read_JPG.xpos(),Read_JPG.ypos()+140) 
    
    # print (Read_JPG['file'].getValue())                
    UndistPath=render_Path + "\\undist\\"
    UndistPath=UndistPath.replace("\\","/")
    UVDistortPath=render_Path + "\\uvmap\\"
    UVDistortPath=UVDistortPath.replace("\\","/")
    UndistFolder=os.listdir(UndistPath)
    for folders in UndistFolder:
        SplitFolderName= folders.split("_")
        Reversed_SplitFolderName = reversed(SplitFolderName)
        print ("OriginalSplitFolderName = {}".format(SplitFolderName))
        LastSLOG = SplitFolderName[-1]
    #    UndistFolderName="_".join(SplitFolderName)
        if LastSLOG=="undist" or LastSLOG =="undistorted":
            for index,v in enumerate(Reversed_SplitFolderName):
                if LastSLOG=="undist" or LastSLOG =="undistorted":
                    if "v00" in v:
                        (SplitFolderName[-index-1]) = Version
                        break

                UndistFolderName="_".join(SplitFolderName)
            print ("UndistFolderName         = {}".format(UndistFolderName))
            print ("LastSLOG         = {}".format(LastSLOG))
            print ("SplitFolderName         = {}".format(SplitFolderName))
    
    print ("UVDistortPath = {}".format(UVDistortPath))
    print ("UndistPath = {}".format(UndistPath))
    try:
        for UnD in nuke.getFileNameList(UndistPath + UndistFolderName):
            Split = UnD.split(" ")
            Split.pop()
            Split = "".join(Split)
            if Split.endswith(".jpg"):
                Read_Undist = nuke.createNode('Read')
                Read_Undist.knob('file').fromUserText(UndistPath + UndistFolderName + "/" + UnD)
    except UnboundLocalError:
        nuke.message("""Missing Undist! Undist Folder should end with '_undist' """)
        #nuke.scriptExit()
    Read_Undist.setXYpos(Read_JPG.xpos()-140,Read_JPG.ypos())
    STNodeUndist = nuke.createNode('STMap')
    STNodeUndist['uv'].setValue("rgba")
    STNodeUndist.setXYpos(Read_Undist.xpos(),Read_Undist.ypos()+140)
    
    for UV in os.listdir(UVDistortPath):
        if "undi".lower() in UV.lower():
            Split_UN,ext = os.path.splitext(UV)
            SplitDist_Undist = Split_UN.split("_")
            print ("SplitDist_Undist = {}".format(SplitDist_Undist))
            for u in SplitDist_Undist:
                if "v0" in u:
                    LastVersion_Undist = u
                    print ("LastVersion_Undist = {}".format(LastVersion_Undist))
        if "redi".lower() in UV.lower():
            Split_RE,ext = os.path.splitext(UV)
            SplitDist_Redist = Split_RE.split("_")
            print ("SplitDist_Redist = {}".format(SplitDist_Redist))
            for r in SplitDist_Redist:
                if "v0" in r:
                    LastVersion_Redist = r
                    print ("LastVersion_Redist = {}".format(LastVersion_Redist))

        try:
            LastVersion_Undist
            LastVersion_Redist
        except NameError:
            pass
    
    
    for uv in os.listdir(UVDistortPath):
        print (uv)
        if "undist_{}".format(LastVersion_Undist).lower() in uv.lower():
            Read_UndistortEXR = nuke.createNode('Read')
            Read_UndistortEXR.knob('file').fromUserText(UVDistortPath + uv)
            Read_UndistortEXR.setXYpos(STNodeJPG.xpos()+150,STNodeJPG.ypos()-20)
            STNodeJPG.setInput(1,Read_UndistortEXR)
        elif "redist_{}".format(LastVersion_Redist).lower() in uv.lower():
            Read_RedistortEXR = nuke.createNode('Read')
            Read_RedistortEXR.knob('file').fromUserText(UVDistortPath + uv)
            Read_RedistortEXR.setXYpos(STNodeUndist.xpos()-150,STNodeUndist.ypos()-20)
            STNodeUndist.setInput(1,Read_RedistortEXR)
        else:
            nuke.message("UV maps wrongly named. Should be _undist_v001 and _redist_v001")
    # nkPath = os.path.join( nkDir, '%s.nk' % nkName )
    SaveNukePath = "{}".format(ThreeD_comp_Path) + "\\" + "nuke" + "\\" + "UV\\"
    print ("SaveNukePath = {}".format(SaveNukePath))
    if not os.path.exists(SaveNukePath):
        original_umask = os.umask(0)
        os.makedirs(SaveNukePath,mode=0o777  )

    JPG = Read_JPG
    JPGFormat = JPG['format'].value()
    JPGPixelAspect = JPG.pixelAspect()
    print ("JPGFormat = {}".format(JPGFormat))
    print ("JPGPixelAspect = {}".format(JPGPixelAspect))

    Undist = Read_Undist
    UndistFormat = Undist['format'].value()
    UndistPixelAspect = Undist.pixelAspect()
    print ("UndistFormat = {}".format(UndistFormat))
    print ("UndistPixelAspect = {}".format(UndistPixelAspect))

    if UndistPixelAspect != JPGPixelAspect:
        UndistFormat.setPixelAspect(JPGPixelAspect)
    else:
        print("Pixel Aspects are the same")
    newUndistPixelAspect= UndistFormat.pixelAspect()
    print ("newUndistPixelAspect = {}".format(newUndistPixelAspect))
    try:
        Viewer = nuke.nodes.Viewer()
        Viewer.setXYpos(STNodeJPG.xpos()-70, STNodeJPG.ypos()+60)
        Viewer.setInput(0, STNodeJPG)
        Viewer.setInput(1, Read_Undist)
        Viewer.setInput(2, STNodeUndist)
        Viewer.setInput(3, Read_JPG)
        nuke.show(Viewer)
    except:
        pass

    UNDIST_BACKDROP = [Read_JPG,BlackOutsideNode,STNodeJPG,Read_UndistortEXR]
    REDIST_BACKDROP = [Read_Undist,STNodeUndist,Read_RedistortEXR]
    print (UNDIST_BACKDROP)
    print (REDIST_BACKDROP)

    for w in nuke.allNodes():
        w.setSelected(False)
    for a in UNDIST_BACKDROP:
        a.setSelected(True)

    BackDropUndist = nukescripts.autoBackdrop()
    BackDropUndist.setName("undist")
    BackDropUndist['bdwidth'].setValue(BackDropUndist['bdwidth'].value()*1.05)
    BackDropUndist['bdheight'].setValue(BackDropUndist['bdheight'].value()*1.18)
    BackDropUndist['tile_color'].setValue(2118008320)
    BackDropUndist['label'].setValue("undist")
    BackDropUndist['note_font'].setValue("Verdana")
    BackDropUndist['note_font_size'].setValue(42)
    BackDropUndist['note_font_color'].setValue(0)
    for w in nuke.allNodes():
        w.setSelected(False)
    for b in REDIST_BACKDROP:
        b.setSelected(True)
    BackDropRedist = nukescripts.autoBackdrop()
    BackDropRedist.setName("redist")
    BackDropRedist['bdwidth'].setValue(BackDropRedist['bdwidth'].value()*1.05)
    BackDropRedist['bdheight'].setValue(BackDropRedist['bdheight'].value()*1.18)
    BackDropRedist['tile_color'].setValue(1048460800)
    BackDropRedist['label'].setValue("redist")
    BackDropRedist['note_font'].setValue("Verdana")
    BackDropRedist['note_font_size'].setValue(42)
    BackDropRedist['note_font_color'].setValue(0)




    for a in nuke.allNodes():
        a.setSelected(True)
    BackDrop = nukescripts.autoBackdrop()
    BackDrop.setName("apply_remove_lens_distortion")
    BackDrop['bdwidth'].setValue(BackDrop['bdwidth'].value()*1.05)
    BackDrop['bdheight'].setValue(BackDrop['bdheight'].value()*1.17)
    BackDrop['tile_color'].setValue(948866560)

    nuke.selectAll()
    nuke.zoomToFitSelected()
    for node in nuke.selectedNodes():
        node.knob("selected").setValue(False)

    if StudioName == "ILP":
        VertVersion = []

        for n in Version:
            if "v".lower() not in n:
                VertVersion.append(n)
        Version = "".join(VertVersion)
        nuke.scriptSaveAs(SaveNukePath +"{}".format(ShotName) +"_lensDistort_" + "vert_" + Version + ".nk", overwrite=1)
    else:
        nuke.scriptSaveAs(SaveNukePath +"{}".format(ShotName) +"_distort_" + Version + ".nk", overwrite=1) 
        pass


def Create_Nuke_File_Mixed(ShotName, ThreeD_comp_Path,render_Path,jpg_Path,Version,UV_LD_Status):
    for a in nuke.allNodes():
        nuke.delete(a)


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
            pass
    for LD in os.listdir(LDNodePath):
        try:
            if "dist_{}".format(LastVersion).lower() in LD.lower():
            #    Create_LD_Node(ShotName, ThreeD_comp_Path,render_Path,jpg_Path,Version)
                print ("Found")
                LD_Check = True
                break
        except:
            pass
    
    print ("LD_Check = {}".format(LD_Check))

    if UV_LD_Status == "UV Map":
        if Redist_Check == True and Undist_Check == True:
            Create_Nuke_File(ShotName, ThreeD_comp_Path,render_Path,jpg_Path,Version)
        else:
            nuke.message("Missing Undistort/Redistort map. Should be named '_redistort_v001' and '_undistort_v001' ")
            #nuke.scriptExit()
    elif UV_LD_Status == "LD Node":
        if LD_Check == True:
            Create_LD_Node(ShotName, ThreeD_comp_Path,render_Path,jpg_Path,Version)
        else:
            nuke.message("Missing LD Node in 'nuke' folder. Should be named 'dist_v001' ")
            #nuke.scriptExit()

#    except:
#        nuke.message("Anomally, check UV Map/LD Node naming, check if 'nuke' folder exists")

#ShotName = "Shadowbone2_207_207-039-5900_MP1_v001"
#ThreeD_comp_Path = r"\\fs3\TPN\CraftyApes\Origami\3d_comp\Shadowbone2_207_207-039-5900_MP1_v001"
#render_Path = r"\\fs3\TPN\CraftyApes\Origami\render\Shadowbone2_207_207-039-5900_MP1_v001"
#jpg_Path = r"\\fs3\TPN\CraftyApes\Origami\input\CRA_Vertigo_2022.11.16\Shadowbone2_207_207-039-5900_MP1_v001\jpg"
#Version = "v001"

#Create_Nuke_File_Mixed(ShotName, ThreeD_comp_Path,render_Path,jpg_Path,Version)