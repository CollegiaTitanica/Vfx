import socket,shutil
import os,subprocess
from _thread import *
ServerSideSocket = socket.socket()
HOST, PORT = "10.100.20.139", 9999
ThreadCount = 0
try:
    
    ServerSideSocket.bind((HOST, PORT))
except socket.error as e:
    print(str(e))
print('Socket is listening..')
ServerSideSocket.listen(5)
######################################################################################
from threading import Timer
from time import sleep
from pathlib import Path
from shutil import rmtree
import threading

class TipettChecker(object):
   # def __init__(self,interval,function,*args,**kwargs):
    def __init__(self,interval,function, RenderPathFolder,ext,Nuke_FileName,RoyalCommand,RenderPath,Frame_Range):
        self._timer      = None
        self.interval     = interval
        self.function     = function
        self.RenderPathFolder = RenderPathFolder
        self.ext            = ext
        self.Nuke_Filename = Nuke_FileName
        self.RoyalCommand  = RoyalCommand
        self.RenderPath    = RenderPath
        self.Frame_Range   = Frame_Range
    #    self.args         = args
    #    self.kwargs       = kwargs
        self.is_running   = False
        self.start()
        self.inkrement = 0
        self.StudioName   = "Tippett"
        self.ext = os.path.splitext(self.RenderPath)[-1]
        self.ext = self.ext.replace("'","")


    def run(self):
        self.is_running = False
        self.start()
        self.function(self)
    
    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval,self.run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

    def CheckTippettStatus(self):
        self.NukeLogs = r"\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\NukeLogs\\"
        Tippett_Actif_File = self.NukeLogs + "Tippett_Actif.txt"
        with open(Tippett_Actif_File) as Actif:
            Tippett_Actif_Text = Actif.readlines()
            for line in Tippett_Actif_Text:
                if "TippetShotActive" in line:
                    line = line.split("=")[-1]
                    TippettBoolean = line
                    print ("line = {}".format(line))
            print ("Tippett_Actif_Text = {}".format(Tippett_Actif_Text))
        
        self.inkrement+= 1
        print ("inkrement = {}".format(self.inkrement))
        
        if TippettBoolean == "False":
            self.stop()
            self.TippettRender()

    def TippettRender(self,**kwargs):
        
        with open ("{}/Tippett_Actif.txt".format(self.NukeLogs),"w") as file:
            TippettTruth = "TippetShotActive=True"
            file.writelines(TippettTruth)
        Args =[r"C:\Program Files\Nuke13.1v3\Nuke13.1.exe", r"\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\Nuke_RenderFrameServer_2.8.py", self.Nuke_Filename,self.RoyalCommand,self.RenderPath,self.Frame_Range]
        Executa = subprocess.run(Args)
        print("Tippett Phase 1 Completed")
        Args2 =[r"C:\Program Files\Nuke13.1v3\Nuke13.1.exe", r"\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\Nuke_Create_Tippett_NukeFile.py", self.RenderPathFolder,self.RenderPath,self.Frame_Range,self.Nuke_Filename]
        Executa2 = subprocess.run(Args2)
        print("Tippett Phase 2 Completed")
        Args3 =[r"C:\Program Files\Nuke13.1v3\Nuke13.1.exe", r"\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\Nuke_PostMortem.py", self.RenderPathFolder,self.RenderPath,self.Frame_Range,self.Nuke_Filename]
        Executa3 = subprocess.run(Args3)
        print("Tippett Phase 3 Completed")

        for pngs in os.listdir(self.RenderPathFolder):
            if pngs.endswith(self.ext):
                os.remove(os.path.join(self.RenderPathFolder,pngs))
            elif pngs.endswith(".nk"):
                os.remove(os.path.join(self.RenderPathFolder,pngs))
            elif pngs.endswith(".tmp"):
                os.remove(os.path.join(self.RenderPathFolder,pngs))
        with open ("{}/Tippett_Actif.txt".format(self.NukeLogs),"w") as file:
            TippettTruth = "TippetShotActive=False"
            file.writelines(TippettTruth)

class MayaRenderGet(TipettChecker):
    def __init__(self,interval,function,DesktopRenderPath,RenderPath,FrameRange,LayerNumber):
        self._timer      = None
        self.interval     = interval
        self.function     = function
        self.RenderPath    = RenderPath
        self.DesktopRenderPath = DesktopRenderPath
        self.FrameRange    = FrameRange
        self.LayerNumber   = LayerNumber
        self.is_running   = False
        self.start()
        self.inkrement = 0
        try:
            self.RemovePreviousRender()
        except:
            pass
        self.ShotName = self.RenderPath.split("/")
        for j in self.ShotName[::-1]:
            self.ShotName.remove(j)
            if j == "main3d":
                break
        self.ShotName = self.ShotName[-2]
        print ("self.ShotName = {}".format(self.ShotName))
        print ("self.RenderPath = {}".format(self.RenderPath))
        print ("self.FrameRange = {}".format(self.FrameRange))

    def RemovePreviousRender(self):
        for path in Path(self.DesktopRenderPath).glob("**/*"):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                rmtree(path)
    
    def GetMayaRenderStatus(self):
        self.MayaLogs = r"\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\MayaLogs\\"
    #    self.MayaRenderFile = self.MayaLogs + "MayaRenderProgress.txt"
        self.MayaRenderFile = self.MayaLogs + "{}.txt".format(self.ShotName)
    #    with open(self.MayaRenderFile) as mrf:
    #        MayaRenderText = mrf.readlines()
    #        for line in MayaRenderText:
    #            if "{}".format(self.ShotName) in line:
    #                line = line.split("=")[-1]
    #                MayaPercentage = line
    #                print ("MayaPercentage = {}".format(MayaPercentage))
    #        print ("MayaRenderText = {}".format(MayaRenderText))
        frame_ranges = self.FrameRange.split("-")
        frame_ranges_FIRSTFRAME = frame_ranges[0]
        frame_ranges_FIRSTFRAME = int(frame_ranges_FIRSTFRAME)
        frame_ranges_LASTFRAME = int(frame_ranges[1])
        print ("frame_ranges_FIRSTFRAME = {}".format(frame_ranges_FIRSTFRAME))
        print ("frame_ranges_LASTFRAME = {}".format(frame_ranges_LASTFRAME))
        self.ImageCount = (frame_ranges_LASTFRAME - frame_ranges_FIRSTFRAME) + 1
        print ("self.ImageCount = {}".format(self.ImageCount))
        self.CompleteImageCount = self.ImageCount * self.LayerNumber
        print ("self.CompleteImageCount = {}".format(self.CompleteImageCount))
        count = 0
        for root_dir, cur_dir, files in os.walk(self.DesktopRenderPath):
            count += len(files)
        print('file count:', count)
        self.MayaPercentage = (count / self.CompleteImageCount) * 100
        self.MayaPercentage = int(self.MayaPercentage)
        print ("self.MayaPercentage = {}".format(self.MayaPercentage))
    ###################################################################   
        mayaTruth = "{}={}".format(self.ShotName,self.MayaPercentage)
         
        with open (self.MayaRenderFile,"w") as file:
            file.writelines(mayaTruth)
                   
            
    ###################################################################
        self.inkrement+= 1
        print ("inkrement = {}".format(self.inkrement))
        
        if self.MayaPercentage == 100:
            self.stop()



######################################################################################
def Le_Printes():
    print("Le Finished.......................................")

def IronClad_Transfer(DesktopMayaRenderPath,MayaRenderPath):
    for folder in os.listdir(DesktopMayaRenderPath):
    #    shutil.move(DesktopMayaRenderPath + "/" + folder,MayaRenderPath)
    #    shutil.move(os.path.join(DesktopMayaRenderPath,folder),MayaRenderPath)
        try:
            shutil.rmtree(os.path.join(MayaRenderPath,folder),ignore_errors=True)
            shutil.move(os.path.join(DesktopMayaRenderPath,folder),MayaRenderPath)
        except: 
            pass

def multi_threaded_client(connection):
    connection.send(str.encode('Server is working:'))
    while True:
#        try:
    #    NukeBoolean = connection.recv(2048).strip().decode('utf-8')
        NukeBoolean,data,dmrp, mrp, FramePath,LayerCount = [i for i in connection.recv(2048).decode('utf-8').split('\n')]
        print("RoyalCommand = {}".format(data))
        print("dmrp = {}".format(dmrp))
        print("mrp = {}".format(mrp))
        print("NukeBoolean = {}".format(NukeBoolean))
        print("FramePath = {}".format(FramePath))

#        except:
#            pass
        if NukeBoolean=="True":
            print("Nuke SHit")
            Nuke_FileName = r"'{data}'".format(data=data)
            Frame_Range= r"'{dmrp}'".format(dmrp=dmrp)
            WriteNode = r"'{mrp}'".format(mrp=mrp)
            RenderPath = r"'{FramePath}'".format(FramePath=FramePath)
            StudioName = LayerCount
            RoyalCommand = """FnNsFrameServer.renderFrames({Nuke_FileName}, {Frame_Range}, {WriteNodes}, ["main"])""".format(Nuke_FileName=Nuke_FileName,Frame_Range=Frame_Range,WriteNodes=WriteNode)
            response = 'Server message: ' + RoyalCommand
            print("RoyalCommand = {}".format(RoyalCommand))
            print("FrameRange = {}".format(Frame_Range))
            print("WriteNode = {}".format(WriteNode))
            print("Nuke_FileName = {}".format(Nuke_FileName))
            print("RenderPath = {}".format(RenderPath))
        #    StudioName = Nuke_FileName.split("/")

        #    for j in StudioName[::-1]:
        #        StudioName.remove(j)
        #        if j == "3d_comp":
        #            break
        #    StudioName=StudioName[-2]
            print("StudioName = {}".format(StudioName))
            RenderPathFolder = RenderPath.split("/")[:-1]
            RenderPathFolder="/".join(RenderPathFolder)
            RenderPathFolder=RenderPathFolder.replace("'","")
            print("RenderPathFolder = {}".format(RenderPathFolder))

            ext = os.path.splitext(RenderPath)[-1]
            ext = ext.replace("'","")
            print("ext = {}".format(ext))

            NukeLogs = r"\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\NukeLogs\\"
            if StudioName == "Tippett":
                Tippett_Actif_File = NukeLogs + "Tippett_Actif.txt"
                with open(Tippett_Actif_File) as Actif:
                    Tippett_Actif_Text = Actif.readlines()
                    for line in Tippett_Actif_Text:
                        if "TippetShotActive" in line:
                            line = line.split("=")[-1]
                            TippettBoolean = line
                            print ("line = {}".format(line))
                    print ("Tippett_Actif_Text = {}".format(Tippett_Actif_Text))
                
                if TippettBoolean == "False":
                    with open ("{}/Tippett_Actif.txt".format(NukeLogs),"w") as file:
                        TippettTruth = "TippetShotActive=False"
                        file.writelines(TippettTruth)
                    Args =[r"C:\Program Files\Nuke13.1v3\Nuke13.1.exe", r"\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\Nuke_RenderFrameServer_2.8.py", Nuke_FileName,RoyalCommand,RenderPath,Frame_Range,"None",StudioName]
                    #Executa = subprocess.run(Args)
                    Executa = subprocess.Popen(Args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

                def check_and_terminate():
                    #Check condition
                    while not condition_met():
                        sleep(1)
                    Executa.terminate()

                def condition_met():
                    New_NukeName = Nuke_FileName.replace("'","")
                    Nuke_ActualFileName = New_NukeName.split("/")[-1]
                    NukeLogs = r"\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\NukeLogs\\"
                    NukeRenderFile = NukeLogs + "{}.txt".format(Nuke_ActualFileName)
                    with open(NukeRenderFile) as nrf:
                        NukeRenderText = nrf.readlines()
                        for line in NukeRenderText:
                            if "{}".format(Nuke_ActualFileName) in line:
                                line = line.split("=")[-1]
                                NukeTruth = line
                                print ("NukeTruth = {}".format(NukeTruth))
                    if NukeTruth == "True":
                        Cancel_Boolean = True
                    else:
                        Cancel_Boolean = False

                    if Cancel_Boolean == True:
                        return True
                    else:
                        return False
                    
                timer_thread = threading.Thread(target=check_and_terminate)
                timer_thread.start()

                return_code = Executa.wait()

                output, error = Executa.communicate()

                output_str = output.decode("utf-8") 
                error_str = error.decode("utf-8") 
                print("Tippett Phase 1 Completed")
                print("Return code", return_code)
                print("Output", output_str)
                print("Error", error_str)
                #print(Executa)
                response = "JOB'S DONE!!"
                connection.send(str.encode(response))
            
                with open ("{}/Tippett_Actif.txt".format(NukeLogs),"w") as file:
                    TippettTruth = "TippetShotActive=False"
                    file.writelines(TippettTruth)

            else:
                Args =[r"C:\Program Files\Nuke13.1v3\Nuke13.1.exe", r"\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\Nuke_RenderFrameServer_2.8.py", Nuke_FileName,RoyalCommand,RenderPath,Frame_Range,"None",StudioName]
                Executa = subprocess.Popen(Args,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                def check_and_terminate():
                    #Check condition
                    while not condition_met():
                        sleep(1)

                    Executa.terminate()

                def condition_met():
                    New_NukeName = Nuke_FileName.replace("'","")
                    Nuke_ActualFileName = New_NukeName.split("/")[-1]
                    NukeLogs = r"\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\NukeLogs\\"
                    NukeRenderFile = NukeLogs + "{}.txt".format(Nuke_ActualFileName)
                    with open(NukeRenderFile) as nrf:
                        NukeRenderText = nrf.readlines()
                        for line in NukeRenderText:
                            if "{}".format(Nuke_ActualFileName) in line:
                                line = line.split("=")[-1]
                                NukeTruth = line
                                print ("NukeTruth = {}".format(NukeTruth))
                    if NukeTruth == "True":
                        Cancel_Boolean = True
                    else:
                        Cancel_Boolean = False

                    if Cancel_Boolean == True:
                        return True
                    else:
                        return False
                    
                timer_thread = threading.Thread(target=check_and_terminate)
                timer_thread.start()

                return_code = Executa.wait()

                output, error = Executa.communicate()

            #    output_str = output.decode("utf-8") 
            #    error_str = error.decode("utf-8") 

            #    print("Return code", return_code)
            #    print("Output", output_str)
            #    print("Error", error_str)
                #print(Executa)
                response = "JOB'S DONE!!"
                try:
                    RenderPathFolder = RenderPath.split("/")[:-1]
                    RenderPathFolder="/".join(RenderPathFolder)
                    RenderPathFolder=RenderPathFolder.replace("'","")
                    print("RenderPathFolder = {}".format(RenderPathFolder))

                    for pngs in os.listdir(RenderPathFolder):
                        if pngs.endswith(".png"):
                            os.remove(os.path.join(RenderPathFolder,pngs))
                        elif pngs.endswith(".nk"):
                            os.remove(os.path.join(RenderPathFolder,pngs))
                        elif pngs.endswith(".tmp"):
                            os.remove(os.path.join(RenderPathFolder,pngs))
                except:
                    pass

                try:
                    connection.send(str.encode(response))
                except ConnectionAbortedError:
                    pass
            break

        elif NukeBoolean=="False":
            print("Maya SHit")
#            try:
#                data,dmrp, mrp = [i for i in connection.recv(2048).decode('utf-8').split('\n')]
#            except:
#                pass
            response = 'Server message: ' + data
            DesktopMayaRenderPath = dmrp
            MayaRenderPath = mrp
            FrameRange = FramePath
            LayerCount = int(LayerCount)
            ShotName = DesktopMayaRenderPath.split("/")[-1]
            print("RoyalCommand = {}".format(data))
            print("DesktopMayaRenderPath = {}".format(dmrp))
            print("MayaRenderPath = {}".format(mrp))
            print("FramePath = {}".format(FramePath))
            if not data:
                break
            elif not dmrp:
                break
            elif not mrp:
                break
            
        #    def RemovePreviousRender():
        #        for path in Path(MayaRenderPath).glob("**/*"):
        #            if path.is_file():
        #               path.unlink()
        #            elif path.is_dir():
        #                rmtree(path)
        #    RemovePreviousRender()

            #connection.sendall(str.encode(response))
            #MayaRenderGet(5,MayaRenderGet.GetMayaRenderStatus,dmrp,mrp,FrameRange,LayerCount)
            Maya=MayaRenderGet(3,MayaRenderGet.GetMayaRenderStatus,DesktopMayaRenderPath,MayaRenderPath,FrameRange,LayerCount)
            ### !!!!!! OLD METHOD !!!!!! ###
            #Executa = subprocess.run(data)
        
            #Executa = subprocess.Popen(data,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            Executa = subprocess.Popen(data,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            
            def check_and_terminate():
                #Check condition
                while not condition_met():
                    sleep(1)
                Executa.terminate()

            def condition_met():

                MayaLogsStatus = r"\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\MayaLogsStatus\\"
                MayaStatusRenderFile = MayaLogsStatus + "{}.txt".format(ShotName)

                with open(MayaStatusRenderFile) as mrf:
                    MayaStatusRenderText = mrf.readlines()
                    for line in MayaStatusRenderText:
                        if "{}".format(ShotName) in line:
                            line = line.split("=")[-1]
                            MayaStatusTruth = line
                           # print ("MayaStatusTruth = {}".format(MayaStatusTruth))
                if MayaStatusTruth == "True":
                    Cancel_Boolean = True
                else:
                    Cancel_Boolean = False

                if Cancel_Boolean == True:
                    return True
                else:
                    return False
                
            timer_thread = threading.Thread(target=check_and_terminate)
            timer_thread.start()

            return_code = Executa.wait()
            output, error = Executa.communicate()
            print("Return code", return_code)
       
            if return_code == 0:
                Maya.MayaPercentage == 100
                Maya.GetMayaRenderStatus()
                Maya.stop()
                IronClad_Transfer(DesktopMayaRenderPath,MayaRenderPath)
                Le_Printes()
                
            elif return_code == 1:
                print("Render Cancelled")
                Maya.stop()
            break

        elif NukeBoolean=="Undist":
            print("UNdist SHit")
#            try:
#                data,dmrp, mrp = [i for i in connection.recv(2048).decode('utf-8').split('\n')]
#            except:
#                pass
            response = 'Server message: ' + data
            Nuke_FileName = r"'{data}'".format(data=data)
            Frame_Range= r"'{dmrp}'".format(dmrp=dmrp)
            WriteNode = r"'{mrp}'".format(mrp=mrp)
            RenderPath = r"'{FramePath}'".format(FramePath=FramePath)
            RoyalCommand = """FnNsFrameServer.renderFrames({Nuke_FileName}, {Frame_Range}, {WriteNodes}, ["main"])""".format(Nuke_FileName=Nuke_FileName,Frame_Range=Frame_Range,WriteNodes=WriteNode)
            response = 'Server message: ' + RoyalCommand
            print("RoyalCommand = {}".format(RoyalCommand))
            print("FrameRange = {}".format(Frame_Range))
            print("WriteNode = {}".format(WriteNode))
            print("Nuke_FileName = {}".format(Nuke_FileName))
            print("RenderPath = {}".format(RenderPath))
            Undist_Crop="True"

            Args =[r"C:\Program Files\Nuke13.1v3\Nuke13.1.exe", r"\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\Nuke_RenderFrameServer_2.8.py", Nuke_FileName,RoyalCommand,RenderPath,Frame_Range,Undist_Crop]
            Executa = subprocess.Popen(Args,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            
            def check_and_terminate():
                #Check condition
                while not condition_met():
                    sleep(1)
                Executa.terminate()

            def condition_met():
                New_NukeName = Nuke_FileName.replace("'","")
                Nuke_ActualFileName = New_NukeName.split("/")[-1]
                NukeLogs = r"\\fs3\Sh1\uber\Nuke_Scripts\NukeScripts\NukeLogs\\"
                NukeRenderFile = NukeLogs + "{}.txt".format(Nuke_ActualFileName)
                with open(NukeRenderFile) as nrf:
                    NukeRenderText = nrf.readlines()
                    for line in NukeRenderText:
                        if "{}".format(Nuke_ActualFileName) in line:
                            line = line.split("=")[-1]
                            NukeTruth = line
                            print ("NukeTruth = {}".format(NukeTruth))
                if NukeTruth == "True":
                    Cancel_Boolean = True
                else:
                    Cancel_Boolean = False

                if Cancel_Boolean == True:
                    return True
                else:
                    return False
                
            timer_thread = threading.Thread(target=check_and_terminate)
            timer_thread.start()

            return_code = Executa.wait()

            output, error = Executa.communicate()

        #    output_str = output.decode("utf-8") 
        #    error_str = error.decode("utf-8") 

            print("Return code", return_code)
        #    print("Output", output_str)
            #print("Error", error_str)

#
            break

    connection.close()
while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
    
ServerSideSocket.close()




