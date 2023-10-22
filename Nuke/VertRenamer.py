import os
import pprint
from itertools import cycle

#ShotName = "LOU_LF_LF-1610_nativeMP_v001"
ShotName = "106-014-150A_Lustra"
#ShotName =     "Shadowbone2_207_207-037-3600_MP1_v001_camWire_v001"
#FinalName =    "Shadowbone2_207_207-037-3600_MP1-CamWire_Neptune_v001_Saturnx"
#FinalName =    "Shadowbone2_207_207-037-3600_MP1-CamWire_v001"
#FinalName =     "LOU_LF_LF-1610_MP-camWire"
FinalName =     "WitchesS1_106-014-150A"
def Define_Standard(ShotName,FinalName):
    New_ShotName = ShotName.replace("-","_")
    New_Final_ShotName = FinalName.replace("-","_")

    ShotName_SPLIT = ShotName.split("_")
    Final_ShotName_SPLIT = FinalName.split("_")

    Heiphen_List = []
    UnderHiphen_List = []
    ExcludeNonHiphen_List = []

    for x in Final_ShotName_SPLIT:
        if "-" in x:
            Heiphen_List.append(x)

    for z in Heiphen_List:
        v = z.replace("-","_")
        UnderHiphen_List.append(v)

    #Under_Heiphen_List = "_".join(Heiphen_List)
    #Under_Heiphen_List = Under_Heiphen_List.replace("-","_")

    #UnderHiphen_List = ("_".join(UnderHiphen_List))

    print("Heiphen_List = "f"{Heiphen_List}")
    print("UnderHiphen_List = "f"{UnderHiphen_List}")


    New_ShotName_SPLIT = New_ShotName.split("_")
    New_Final_ShotName_SPLIT = New_Final_ShotName.split("_")
    seen = set()
    duples = [x for x in New_ShotName_SPLIT if x in seen or seen.add(x)]

#    print("ShotName_SPLIT =     "f"{ShotName_SPLIT}")
#    print("Final_ShotName_SPLIT = "f"{Final_ShotName_SPLIT}")

    print("New_ShotName_SPLIT =     "f"{New_ShotName_SPLIT}")
    print("New_Final_ShotName_SPLIT = "f"{New_Final_ShotName_SPLIT}")
    print("duples = "f"{duples}")

    Untouched = []
    Remove = []
    Add = []
    AddIndexList = []
    RemoveIndexList = []


    HeiphenIndex = []
    LustraList = []
    NEWUnderHiphen_List=[]
    for k in UnderHiphen_List:
        k = k.split("_")
        NEWUnderHiphen_List.append(k)

    print("NEWUnderHiphen_List = "f"{NEWUnderHiphen_List}")

    HiphenIndexList = []

    #for idx,elem in enumerate(HiphenIndexList):
    #        innerlist = []
    #        for IDX in elem:
    #            innerlist.append(New_ShotName_Split[IDX])
    #            EleminateIndexFull.append(IDX)
    #        Appendix1.append(innerlist)
    #        InsertIndex.append(min(elem))
    licycle = cycle(New_Final_ShotName_SPLIT)
   # kicycle = cycle(NEWUnderHiphen_List[0])
    # Prime the pump
    nextelem = next(licycle)
   # kextelem = next(kicycle)

    for index,k in enumerate(NEWUnderHiphen_List):
        LenthOfUnderList = len(k)
        kicycle = cycle(NEWUnderHiphen_List[index])
        intralist=[]
        lustralist = []
        for l,ex in enumerate(New_Final_ShotName_SPLIT):

         #   nextelem = next(licycle)
            if ex in k:
                thiselem = nextelem
                nextelem = next(licycle)
                kextelem = next(kicycle)

                for x in k:
                    nextelem = next(licycle)

                    if nextelem == x:
                        break
                    else:
                        lustralist.append(l)  
                intralist.append(l)      
        if intralist != []:
            HeiphenIndex.append(intralist)
            LustraList.append(lustralist)
 #   print("HeiphenIndex = "f"{HeiphenIndex}")

    for v in LustraList:
        v = list(set(v))
        HiphenIndexList.append(v)
    print("HiphenIndexList = "f"{HiphenIndexList}")
# Which words were deleted in Final ShotName
    for index,k in enumerate(New_ShotName_SPLIT):
        if k not in (New_Final_ShotName):
            Remove.append(k)
            RemoveIndexList.append(index)
        else:
            for invex,j in enumerate(New_Final_ShotName_SPLIT):
                if index == invex and k != j and k in duples:
                    Remove.append(k)
                    RemoveIndexList.append(index)
                if k == j:
                    break
#                elif k != j:
#                    break
#                elif invex==index:
#                    Remove.append(k)
#                    RemoveIndexList.append(index)

# Which words were added in Final ShotName
    for index,k in enumerate(New_Final_ShotName_SPLIT):
        if k in New_ShotName_SPLIT:
            for invex,j in enumerate(New_ShotName_SPLIT):
                if k != j:
                    break
                elif k == j:
                    break
                elif invex==invex:
                    Add.append(k)
                    AddIndexList.append(index)
            pass
        else:
            Add.append(k)
            AddIndexList.append(index)
#    for index,k in enumerate(New_Final_ShotName_SPLIT):

#        for invex,j in enumerate(New_ShotName_SPLIT):
#            if k != j:
#                break
#            elif invex==invex:
#                Add.append(k)
#                AddIndexList.append(index)
#            else:
#                Add.append(k)
#                AddIndexList.append(index)

 #   print("Untouched = "f"{Untouched}")
    print("Remove = "f"{Remove}")
    print("RemoveIndexList = "f"{RemoveIndexList}")
    print("AddIndexList = "f"{AddIndexList}")
    print("Add = "f"{Add}")


    return Add,AddIndexList,RemoveIndexList,HiphenIndexList

def multipop(yourlist, itemstopop):
    result = []
    itemstopop.sort()
    itemstopop = itemstopop[::-1]
    for x in itemstopop:
        result.append(yourlist.pop(x))
    return result


Add,AddIndexList,RemoveIndexList,HiphenIndexList = Define_Standard(ShotName,FinalName)


#ShotName = "Shadowbone2_207_207-042-3300_MP1_v002_camWire_v001"
#ShotName = "LOU_LF_LF-1130_nativeMP_v001"
ShotName = "105-018-190A_Lustra"
#Add = ["Neptune","Saturnx"]
#AddIndexList=[7,9]
#RemoveIndexList=[6]
#HiphenIndexList=[[2,3,4],[5,6]]
def VertRename(ShotName,RemoveIndexList,HiphenIndexList):

    ShotName_Split = ShotName.split("_")
    print("ShotName_Split = "f"{ShotName_Split}")
    New_ShotName_Split = ShotName.replace("-","_")
    New_ShotName_Split = New_ShotName_Split.split("_")
    print("Old_ShotName_Split = "f"{New_ShotName_Split}")
    L = multipop(New_ShotName_Split,RemoveIndexList)
    print("L = "f"{L}")

    # Add words into the specified Index
    for ifx,word in enumerate(Add):
        New_ShotName_Split.insert(AddIndexList[ifx],word)


    print("New_ShotName_Split = "f"{New_ShotName_Split}")

    Appendix1 = []
    
    EleminateIndexFull=[]
    InsertIndex =[]
    ExterminateIndex = EleminateIndexFull
    for idx,elem in enumerate(HiphenIndexList):
        innerlist = []
        for IDX in elem:
            innerlist.append(New_ShotName_Split[IDX])
            EleminateIndexFull.append(IDX)
        Appendix1.append(innerlist)
        InsertIndex.append(min(elem))
    print("Appendix1 = "f"{Appendix1}")
    print("EleminateIndexFull = "f"{EleminateIndexFull}")
    print("InsertIndex = "f"{InsertIndex}")

    for x in ExterminateIndex:
        for y in InsertIndex:
            if y in ExterminateIndex:
                ExterminateIndex.remove(y)
    print("ExterminateIndex = "f"{ExterminateIndex}")

    New_Appendix1 = Appendix1
    New_Appendix2 = []
    for idx,elem in enumerate(New_Appendix1):
        innerlist = []
        a= "-".join(elem)       
        New_Appendix2.append(a)
    print("New_Appendix2 = "f"{New_Appendix2}")
    
    test_New_ShotName_Split = New_ShotName_Split

#    # Add words into the specified Index
#    for ifx,word in enumerate(Add):
#        test_New_ShotName_Split.insert(AddIndexList[ifx],word)
        
    print("test_New_ShotName_Split = "f"{test_New_ShotName_Split}")  
    
    FinalShot = New_ShotName_Split
    for kur,ylem in enumerate(FinalShot):
        for o,r in enumerate(InsertIndex):
            if kur == r:
                FinalShot[kur] = New_Appendix2[o]
    
    multipop(FinalShot,ExterminateIndex)
    print("FinalShot = "f"{FinalShot}")   
    
    
    result= "_".join(FinalShot)
    print(result)
    return result

VertRename(ShotName,RemoveIndexList,HiphenIndexList)