import os 
import maya.cmds as mc


def saveScreenshot(name, directory=''):
    
    #if folder doesnt exist, make folder
    if not os.path.exists(directory):
        os.makedirs(directory)

    path = os.path.join(directory, '%s.jpg' % name)

    mc.viewFit()
    mc.setAttr('defaultRenderGlobals.imageFormat', 8)

    mc.playblast(completeFilename=path, forceOverwrite=True, format='image', width=500, height=500,
                       showOrnaments=False, startTime=1, endTime=1, viewer=False)

    return path
    
    
