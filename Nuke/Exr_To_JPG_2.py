import os,sys,subprocess,glob
import nuke,threading,multiprocessing
import concurrent.futures,shutil
from datetime import datetime,timedelta
from time import mktime

class EXR():
    def __init__(self):
        self.Core_Number = multiprocessing.cpu_count()
        print("The Computer has {}".format(self.Core_Number))
        self.ReadNodeList = []
        AllNodes = nuke.allNodes()
        for node in AllNodes:
            if node.Class() == 'Read' :
                self.ReadNodeList.append(node)
            elif node.Class() == 'SoftClip' :    #Delete any SoftClip and Write Nodes from previous script activation
                nuke.delete(node)
            elif node.Class() == 'Write' :
                nuke.delete(node)
            elif node.Class() == 'Viewer' :
                nuke.delete(node)

        self.ExrToJpg()

    def GetPadding(self):
        try:
            for image in os.listdir(self.EXR_Link):
                Split = image.split(".")
                Split.pop()
                Split = Split[-1]
                NumberCount = 0
                for l in Split:
                    NumberCount += 1
            
                return NumberCount
        except FileNotFoundError:
            nuke.message("EXR not Found!")
        #  sys.exit()

    def Make_Folders(self):
        if not os.path.exists(self.Input_Link):
            os.makedirs(self.Input_Link)
        if not os.path.exists(self.EXR_Path):
            os.makedirs(self.EXR_Path)
        if not os.path.exists(self.JPG_Path):
            os.makedirs(self.JPG_Path)

    def copy_files(worker_id):
        while True:
            try:
                with lock:
                    src_file = file_queue.get_nowait()
                
            except queue.empty:
                break

            else:
                self.copy_file(src_file)
                with lock:
                    file_queue_task_done()

    def copy_file(self,source_file):   
        src_path = os.path.join(self.EXR_Link,source_file)
        src_path = src_path.replace("/","\\")
        dst_path = os.path.join(self.EXR_Path,source_file+"*")

    #    os.chmod(src_path,stat.S_IWRITE)
    #    os.chmod(dst_path,stat.S_IWRITE)
    #    subprocess.call(f"xcopy /Y \"{src_path}\" \"{dst_path}\"",shell=True)
        #subprocess.call(["xcopy",f"{src_path}",f"{dst_path}","/y"])
        #subprocess.call(["xcopy",f"{src_path}",f"{dst_path}","/Y","/i","/f"])
        subprocess.call(["xcopy","/F","/Y",src_path,dst_path])
        


    def Try_New_Copy(self):
        self.file_list = os.listdir(self.EXR_Link)
        with concurrent.futures.ThreadPoolExecutor(max_workers=60) as executor:
            futures = [executor.submit(self.copy_file, file) for file in self.file_list]


        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
            except Exception as exc:
                print(f"File copy failed: {exc}")

    def Copy_EXR_To_Source(self,EXR_Link):
        self.EXR_Link = self.EXR_Link.replace("/","\\")
        Source_EXR_Link = self.EXR_Path
        print ("Source_EXR_Link = {}".format(Source_EXR_Link))
            
        for imazh in os.listdir(self.EXR_Link):
            source = self.EXR_Link + "\\" + imazh
        #    destination = self.Source_EXR_Link + "\\" + imazh
            destination = Source_EXR_Link
        #    shutil.copyfile(source,destination)
            subprocess.call(["xcopy",f"{source}",f"{destination}","/y"])

    def ExrToJpg(self):
        i=0
        for n in self.ReadNodeList:
        
            FilePath = n['file'].getValue()
            first = int(n['first'].getValue())
            last =  int(n['last'].getValue())
            print("first = {}".format(first))
            print ("last = {}".format(last))
            print ("Filepath = {}".format(FilePath))

            extension = os.path.splitext(FilePath)[1]        
            print("Extension = {}".format(extension))

            CleanPath = FilePath.split(".")[0]
            print ("CleanPath = {}".format(CleanPath))
            self.ShotName = CleanPath.split("/")[-1]
            print ("self.ShotName = {}".format(self.ShotName))

            self.EXR_Link = CleanPath.split("/")
            self.EXR_Link.pop()
            self.EXR_Link = "/".join(self.EXR_Link)
            print ("self.EXR_Link = {}".format(self.EXR_Link))

            


            Split_Link = CleanPath.split("//")[-1]
            Split_Link = Split_Link.split("/")
            print ("Split_Link = {}".format(Split_Link))
            for elem in reversed(Split_Link):
                Split_Link.remove(elem)
                if elem == "input":                   
                    break

            self.Input_Link = "\\\\"+"\\".join(Split_Link) + "\\" + "source" + "\\" + "{}".format(self.ShotName)
            self.Input_Link = "\\".join(Split_Link) + "\\" + "source" + "\\" + "{}".format(self.ShotName)
            print ("self.Input_Link = {}".format(self.Input_Link))
            self.ProjectName = Split_Link[-1]
            print ("self.ProjectName = {}".format(self.ProjectName))
            self.StudioName = Split_Link[-2]
            print ("self.StudioName = {}".format(self.StudioName))

            self.EXR_Path = self.Input_Link + "\\exr"
            self.JPG_Path = self.Input_Link + "\\jpg"

            #self.Try_New_Copy()
            #copy_thread = threading.Thread(target=self.Copy_EXR_To_Source,args=(self.EXR_Link,))
            copy_thread = threading.Thread(target=self.Try_New_Copy)
            copy_thread.start()
            #self.Copy_EXR_To_Source(self.EXR_Link)
            self.Make_Folders()


            Padding = self.GetPadding()
            Taraba = ""

            for t in range(Padding):
                Taraba += "#"
            print ("Taraba = {}".format(Taraba)) 




            WritePath = self.JPG_Path + "\\" + self.ShotName + ".{}.jpg".format(Taraba)
            WritePath = WritePath.replace("\\","/")
            print ("WritePath = {}".format(WritePath))


            n.setXYpos(self.ReadNodeList[-1+i].xpos()+200,self.ReadNodeList[0].ypos())
            SoftNode = nuke.createNode('SoftClip')
            SoftNode.setInput(0,n)
            SoftNode.setXYpos(n.xpos(),n.ypos()+120)
            SoftNode['softclip_min'].setValue(0)
            SoftNode['conversion'].setValue('logarithmic compress')
            i=i+1
            WriteNode=nuke.createNode("Write")
            WriteNode.setXYpos(SoftNode.xpos(),SoftNode.ypos()+60)
            if extension == ".exr" or extension == ".dpx":
    
                WriteNode['file'].setValue(WritePath)

            try:
                WriteNode['_jpeg_quality'].setValue(1)
            except:
                pass
            FrameRange = ("{}-{}".format(first,last))
            print ("FrameRange = {}".format(FrameRange)) 
        #   WriteNode['frame_range_string'].setValue(FrameRange)
    #       nukescripts.renderdialog._gRenderDialogState.saveValue('frame_range', 'custom')
    #       nukescripts.renderdialog._gRenderDialogState.saveValue('frame_range_string', FrameRange)
            nukescripts.renderdialog._gRenderDialogState.saveValue('frame_range', 'custom')
            nukescripts.renderdialog._gRenderDialogState.saveValue('frame_range_string', FrameRange)
            
            ViewerNode = nuke.createNode("Viewer")
            ViewerNode.setXYpos(WriteNode.xpos(),WriteNode.ypos()+60)
            nuke.show(ViewerNode)
            self.Check_And_Comapre_Images(self.EXR_Link,self.EXR_Link)
    
    def Check_And_Comapre_Images(self,EXR_Link,EXR_Path):  
        if not os.path.exists(EXR_Path):
            print("EXR Path does not exist.")
            # return

        exr_files = glob.glob(os.path.join(EXR_Path, '*.exr'))
        if not exr_files:
            print("No .exr files in the EXR Path.")
            # return
        
        source_files = glob.glob(os.path.join(EXR_Link, '*.exr'))
        if not source_files:
            print("No .exr files in the Source EXR Link.")

        # Print date of .exr file
        for exr_file in exr_files:
            timestamp = os.path.getmtime(exr_file)
            # print(f"File: {exr_file}, Last modified on: {datetime.fromtimestamp(timestamp)}")
            # Get the current modification time
            current_time = os.path.getmtime(f"{exr_file}")

            current_datetime = datetime.fromtimestamp(current_time)
            # Add one day
            new_datetime = current_datetime + timedelta(days=-1)


            # new_time = mktime(new_datetime.timetuple())

            # os.utime(f"{exr_file}", (new_time, new_time))
        
        
        
        # Image count check
        if len(exr_files) > len(source_files):
            print("EXR folder has more images than the source folder.")
            
        elif len(exr_files) == len(source_files):
            print("EXR folder has equal image count as source folder.")

        # Check date of Source_EXR_Link
        if os.path.exists(EXR_Link):
            timestamp = os.path.getmtime(EXR_Link)
            source_date = datetime.fromtimestamp(timestamp)
            # print(f"Source EXR Link: {EXR_Link}, Last modified on: {source_date}")

            # Compare date of Source_EXR_Link with .exr files
            for exr_file in exr_files:
                exr_file_date = datetime.fromtimestamp(os.path.getmtime(exr_file))
                delta = source_date - exr_file_date  # difference between the two dates
                days = delta.days  # number of days
                seconds = delta.seconds  # number of seconds within a day (not total number of seconds)
                minutes = seconds // 60  # number of minutes within a day
                hours = minutes // 60  # number of hours within a day


                print(f"EXR file {exr_file} is {days} days, {hours % 24} hours, {minutes % 60} minutes, and {seconds % 60} seconds different from Source EXR Link.")


                if days >= 1:
                    print(f"EXR file {exr_file} is at least 1 day older than Source EXR Link.")
                    
                    break
                elif exr_file_date > source_date:
                    print(f"EXR file {exr_file} is newer than Source EXR Link.")
                    break
                elif exr_file_date < source_date:
                    print(f"EXR file {exr_file} is older than Source EXR Link.")
                    break
                else:
                    print(f"EXR file {exr_file} and Source EXR Link were last modified at the same time.")
                    break

        else:
            print("Source EXR Link does not exist.")
    

EXR()

nuke.selectAll()
nuke.zoomToFitSelected()
for node in nuke.selectedNodes():
    node.knob("selected").setValue(False)