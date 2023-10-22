from bdb import checkfuncname
from genericpath import isfile
from multiprocessing.connection import wait
import os
import nuke
import socket
import sys,subprocess,time
from hiero.ui.nuke_bridge import FnNsFrameServer
from hiero.ui.nuke_bridge import FnNsPostProcessorScript
from foundry.frameserver.nuke import renderqueue as rq
#from . import FnNsFrameServer
from threading import Timer
from time import sleep
from pathlib import Path
from shutil import rmtree
import threading

Undist_Crop_Bool = False
Nuke_FileName = str(sys.argv[1])
print("Nuke_FileName = {}".format(Nuke_FileName))
RoyalCommand = str(sys.argv[2])
print("RoyalCommand = {}".format(RoyalCommand))
RenderPath = str(sys.argv[3])
print("RenderPath = {}".format(RenderPath))
Frame_Range = str(sys.argv[4])
print("Frame_Range = {}".format(Frame_Range))
try:
    Undist_Crop = str(sys.argv[5])
    if Undist_Crop != "None":
        print("Undist_Crop = {}".format(Undist_Crop))
        Undist_Crop_Bool = True
except:
    pass

try:
    StudioName = str(sys.argv[6])
except:
    pass


FirstFrame = Frame_Range.split("-")[-2]
LastFrame = Frame_Range.split("-")[-1]
FirstFrame = int(FirstFrame.replace("'",""))
LastFrame = int(LastFrame.replace("'",""))
print("FirstFrame = {}".format(FirstFrame))
print("LastFrame = {}".format(LastFrame))

ImageCount = (LastFrame - FirstFrame) + 1
print("ImageCount = {}".format(ImageCount))

ext = os.path.splitext(RenderPath)[-1]
ext = ext.replace("'","")
print("ext = {}".format(ext))

RenderPathFolder = RenderPath.split("/")[:-1]
RenderPathFolder="/".join(RenderPathFolder)
RenderPathFolder=RenderPathFolder.replace("'","")
RenderPathFolder=RenderPathFolder + "/"

TippettName = os.path.splitext(RenderPath)[-2]
TippettName = TippettName.replace("'","")
TippettName = TippettName.split(".")[:-1]
TippettName = "".join(TippettName)
TippettName = TippettName.split("/")[-1]
TippettName = "".join(TippettName)
print("TippettName = {}".format(TippettName))

print("RenderPathFolder = {}".format(RenderPathFolder))

Nuke_ActualFileName = Nuke_FileName.split("/")[-1]
Nuke_ActualFileName = Nuke_ActualFileName.replace("'","")
print("Nuke_ActualFileName = {}".format(Nuke_ActualFileName))

#StudioName = Nuke_FileName.split("/")

#if not Undist_Crop_Bool:
#    for j in StudioName[::-1]:
#        StudioName.remove(j)
#        if j == "3d_comp":
#            break
#    StudioName=StudioName[-2]
#    print("StudioName = {}".format(StudioName))

class RepeatedTimer(object):
    def __init__(self,interval,function,*args,**kwargs):
        self._timer      = None
        self.interval     = interval
        self.function     = function
        self.args         = args
        self.kwargs       = kwargs
        self.is_running   = False
        self.start()
        self.inkrement = 0
        self.imagesNumber = 0
        self.prevImagesNumber = 0
        self.failCounter = 0
        self.Nuke_The_Nuke_Process()
        try:
            self.RemovePreviousRender()
        except:
            pass

    def run(self):
        self.is_running = False
        self.start()
        self.function(self,*self.args,**self.kwargs)
    
    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval,self.run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

    def RemovePreviousRender(self):
        for path in Path(RenderPathFolder).glob("**/*"):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                rmtree(path)
                
    def ExecuteTippettMOV(self,node):
        nuke.executeInMainThreadWithResult(nuke.execute, args = (node),kwargs = {'continueOnError': True})
        print("Executa is done")
        nuke.executeInMainThreadWithResult(self.NukeClose)
     
    def NukeClose(self):
        nuke.scriptSaveAndClear(ignoreUnsavedChanges=True)
        nuke.scriptExit()

    def TipettPNG_MOV(self):
        try:
            for seq in nuke.getFileNameList(RenderPathFolder):
                if ".png" in seq:
                    TippettPNGReadNode = nuke.nodes.Read()
                    TippettPNGReadNode.knob('file').fromUserText(RenderPathFolder + "/" + seq)
        except:
            TippettPNGReadNode = nuke.nodes.Read()
            print("Something went wrong...")
        try:
            MOVWriteNode = nuke.nodes.Write()
            MOVWriteNode["file"].setValue(RenderPathFolder + "/" + TippettName +".mov")
            MOVWriteNode.setInput(0,TippettPNGReadNode)
            MOVWriteNode["name"].setValue("MOVWriteNode")
        except:
            print("Mov Something wrong")
        try:
            TippettPNGReadNode.setXYpos(MOVWriteNode.xpos(),MOVWriteNode.ypos()-250)
            TippettPNGReadNode["name"].setValue("TippettPNGReadNode")
        except:
            print("Movement Problem")
    #    nuke.selectAll()
    #    nuke.zoomToFitSelected()
    #    for Nukenode in nuke.selectedNodes():
    #        Nukenode.knob("selected").setValue(False)
        
    #    thread = threading.Thread(None, self.ExecuteTippettMOV, args= (MOVWriteNode,)).start()

    def Literally_Nothing(self):
    
    # aapr = Apple Prores
    # jpeg = Photo JPEG
    # mjpa = Motion JPEG A
    
    #    TippettPNGReadNode = nuke.nodes.Read()
    #    for sez in nuke.getFileNameList(RenderPathFolder):
    #        print(sez)
            
        #    
            
        #    TippettPNGReadNode['file'].evaluate()
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
        MOVWriteNode["file"].fromUserText(RenderPathFolderREVERSED + TippettName +".mov")
        MOVWriteNode['file_type'].setValue("mov")
        MOVWriteNode.setInput(0,TippettPNGReadNode)
        MOVWriteNode["name"].setValue("MOVWriteNode")
        MOVWriteNode['mov64_codec'].setValue("jpeg")
        MOVWriteNode['mov64_quality'].setValue("Best")

        MOVWriteNode['mov64_pixel_format'].setValue("{2}")


        TippettPNGReadNode.setXYpos(MOVWriteNode.xpos(),MOVWriteNode.ypos()-250)
        TippettPNGReadNode["name"].setValue("TippettPNGReadNode")

        nuke.scriptSaveAs((RenderPathFolder + Nuke_ActualFileName),1)
        nuke.scriptSaveAndClear(ignoreUnsavedChanges=True)
        nuke.scriptExit()
    #    nuke.executeInMainThreadWithResult(self.NukeClose)
    #    self.thread = threading.Thread(None, self.ExecuteTippettMOV, args= (MOVWriteNode,)).start()

    def CheckForFailiure(self):
        if self.prevImagesNumber < self.imagesNumber:
            self.prevImagesNumber = self.imagesNumber
            print ("self.prevImagesNumber = {}".format(self.prevImagesNumber))
            self.failCounter = 0

        elif self.prevImagesNumber == self.imagesNumber:
            self.failCounter += 1
            print ("self.failCounter = {}".format(self.failCounter))
        
        elif self.prevImagesNumber > self.imagesNumber:
            self.failCounter += 1
            print ("self.failCounter = {}".format(self.failCounter))

    def Nuke_The_Nuke_Process(self):
        self.NukeLogs = r"\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\NukeLogs\\"
        self.NukeRenderFile = self.NukeLogs + "{}.txt".format(Nuke_ActualFileName)
        with open(self.NukeRenderFile) as nrf:
            NukeRenderText = nrf.readlines()
            for line in NukeRenderText:
                if "{}".format(Nuke_ActualFileName) in line:
                    line = line.split("=")[-1]
                    self.NukeTruth = line
                    print ("self.NukeTruth = {}".format(self.NukeTruth))
                    
            print ("NukeRenderText = {}".format(NukeRenderText))
        if self.NukeTruth == "True":
            self.stop()
            nuke.scriptExit()

    def Funzone(self):
        self.images_found=0
        for images in os.listdir(RenderPathFolder):
            if images.endswith(ext):
                self.images_found += 1
            #    print ("self.images_found = {}".format(self.images_found))
        self.imagesNumber = self.images_found
        self.inkrement+= 1
        print ("inkrement = {}".format(self.inkrement))
        print ("self.imagesNumber = {}".format(self.imagesNumber))

        self.Nuke_The_Nuke_Process()
        self.CheckForFailiure()
        if self.failCounter > 7:
            print("ABORTION")
            self.stop()
         #   self.__init__(5,self.Funzone)
            rt = RepeatedTimer(5,RepeatedTimer.Funzone)
            exec(RoyalCommand)

        if self.images_found == ImageCount:
            self.stop()
           ## if StudioName == "Tippett":
            #    self.TipettPNG_MOV()
            #    self.Literally_Nothing()
            #    self.threadTPN = threading.Thread(None, self.Literally_Nothing)
            #    nuke.executeInMainThread(self.threadTPN.start)         
            #    nuke.scriptExit()       
           ## else:
            nuke.scriptExit()
            #    self.stop()

    

rt = RepeatedTimer(12,RepeatedTimer.Funzone)





#postProcessScript(r"\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\Nuke_PostMortem.py")
exec(RoyalCommand)



















