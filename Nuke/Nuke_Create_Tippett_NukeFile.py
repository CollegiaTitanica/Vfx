import os
import nuke
import socket
import sys,subprocess
#from hiero.ui.nuke_bridge import FnNsFrameServer


RenderPathFolder = str(sys.argv[1])
print("RenderPathFolder = {}".format(RenderPathFolder))
RenderPath = str(sys.argv[2])
print("RenderPath = {}".format(RenderPath))
Frame_Range = str(sys.argv[3])
print("Frame_Range = {}".format(Frame_Range))
Nuke_FileName = str(sys.argv[4])
print("Nuke_FileName = {}".format(Nuke_FileName))

Nuke_ActualFileName = Nuke_FileName.split("/")[-1]
Nuke_ActualFileName = Nuke_ActualFileName.replace("'","")
print("Nuke_ActualFileName = {}".format(Nuke_ActualFileName))

TippettName = os.path.splitext(RenderPath)[-2]
TippettName = TippettName.replace("'","")
TippettName = TippettName.split(".")[:-1]
TippettName = "".join(TippettName)
TippettName = TippettName.split("/")[-1]
TippettName = "".join(TippettName)
print("TippettName = {}".format(TippettName))


RenderPathFolder = RenderPath.split("/")[:-1]
RenderPathFolder="/".join(RenderPathFolder)
RenderPathFolder=RenderPathFolder.replace("'","")
RenderPathFolder=RenderPathFolder + "/"

def Create_Tippett_NukeFile(Mov_Standard = True):
    
    # aapr = Apple Prores
    # jpeg = Photo JPEG
    # mjpa = Motion JPEG A
    
    sez = nuke.getFileNameList(RenderPathFolder)[0]
    TippettPNGReadNode = nuke.nodes.Read()
    TippettPNGReadNode['file'].fromUserText(RenderPathFolder + sez)
#    TippettPNGReadNode['file'].setValue(RenderPathFolder + sez)
    
    MOVWriteNode = nuke.nodes.Write()
    
    RenderPathFolderREVERSED=RenderPathFolder
    RenderPathFolderREVERSED=RenderPathFolderREVERSED.replace("\\","/")
    print("RenderPathFolderREVERSED = {}".format(RenderPathFolderREVERSED))
    MOVWriteNode['file_type'].setValue("png")
    #MOVWriteNode["file"].setValue(RenderPathFolderREVERSED + TippettName +".mov")
    if Mov_Standard == True:
        MOVWriteNode["file"].fromUserText(RenderPathFolderREVERSED + TippettName +".mov")
        MOVWriteNode['file_type'].setValue("mov")
        MOVWriteNode["name"].setValue("MOVWriteNode")
        MOVWriteNode['mov64_codec'].setValue("jpeg")
        MOVWriteNode['mov64_quality'].setValue("Best")
        MOVWriteNode['mov64_pixel_format'].setValue("{2}")

    elif Mov_Standard == False:
        MOVWriteNode["file"].fromUserText(RenderPathFolderREVERSED + TippettName +".mp4")
        MOVWriteNode['file_type'].setValue("mov")
        MOVWriteNode["name"].setValue("MOVWriteNode")
        MOVWriteNode['mov64_codec'].setValue("h.264")
        MOVWriteNode['mov64_quality'].setValue("Best")
        MOVWriteNode['mov64_pixel_format'].setValue("{2}")

    MOVWriteNode.setInput(0,TippettPNGReadNode)
    TippettPNGReadNode.setXYpos(MOVWriteNode.xpos(),MOVWriteNode.ypos()-250)
    TippettPNGReadNode["name"].setValue("TippettPNGReadNode")


    nuke.scriptSaveAs((RenderPathFolder + Nuke_ActualFileName),1)
    nuke.scriptSaveAndClear(ignoreUnsavedChanges=True)
    nuke.scriptExit()


#    nuke.executeInMainThreadWithResult(self.NukeClose)
#    self.thread = threading.Thread(None, self.ExecuteTippettMOV, args= (MOVWriteNode,)).start()

Create_Tippett_NukeFile(False)








