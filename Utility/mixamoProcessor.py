
import os
from re import I
import maya.cmds as mc

def GetFilesRecursive(RootDir, Return="Files", MustHaveStrings=""):
    TheDirs= []
    TheFiles = []
    n = 0
    for root, dirs, files in os.walk(RootDir):
        n+=1
        for n in range(0, len(dirs)):
            if ((MustHaveStrings=="") or (dirs[n].find(MustHaveStrings) != -1)):
                TheDirs.append(dirs[n])

        for n in range(0, len(files)):
            if ((MustHaveStrings=="") or (files[n].find(MustHaveStrings) != -1)):
                ThisFile = (root.replace("\\", "/")) + "/" + (files[n])
                TheFiles.append(ThisFile)
            
    if Return == "Files":
        return TheFiles
    else:
        return TheDirs


#this adds the root join and parent the skeleton to it
def parentToRoot():
    mc.joint()
    mc.rename("joint1", "root")
    mc.select("mixamorig1:Hips")
    mc.select("root", add=True)
    mc.parent()

def SetRangeToShowAllKeyframes():
    AllObjs = mc.ls(typ="transform", r=True)
    AllObjs += mc.ls(typ = "joint", r=True)

    FirstFrame= 999999999
    LastFrame = -999999999
    
    for obj in AllObjs:
        FirstFrame = min([FirstFrame, int(mc.findKeyframe(obj, which="first"))])
        LastFrame = max([LastFrame, int(mc.findKeyframe(obj, which="last"))])
    mc.playbackOptions(min=FirstFrame, max=LastFrame)



def do_playblast(PlayblastFilename):
    mc.playblast(format="qt", viewer=False, quality=30, w=633, h=36, clearCache=True, showOrnaments = False, f=PlayblastFilename, p=100, forceOverwrite=True, percent = 100, compression= "H.264", sequenceTime=False, fp=4)


def convert_mxm_animations(folder_path, output_dir):
    files = GetFilesRecursive(folder_path, Return = "Files")

    file_suffix = "_wRoot"

    for mFile in files:


        #how to find stuff or reverse in python
        slashIndex = mFile.rfind('/')
        print (slashIndex)
        # how to get substring in python
        name_string = mFile[slashIndex+1:]
        name_string = name_string.replace(".fbx", file_suffix+".fbx")

        mov_name = name_string.replace(".fbx",".mov")

        #importing an fbx
        mc.file(f=True, new=True)
        mc.file(mFile, i=True)
        #print(name_string)

        SetRangeToShowAllKeyframes()

        


        output_path = output_dir +'\\'+ name_string
        output_mov_path = output_dir+mov_name
        parentToRoot()
        #do_playblast(output_mov_path)

        mc.select("root", replace=True)
        #exporting the fbx

        print("output path is "+ output_path)
        
        mc.file(output_path, exportSelected=True, type='FBX export')


folder_path = "C:\\Users\\ymz19\\Downloads\\animTest"
output_dir = "C:\\Users\\ymz19\\Downloads\\testOutput\\"





