#built in python
import os
import json
import subprocess
import argparse

#ttf site packages

#import performance assembly


#local app
import pymel.core as pm
import maya.cmds as cmds

#load plugins
if not cmds.pluginInfo('mayaHIK', q=True, l=True):
    cmds.loadPlugin('mayaHIK')
if not cmds.pluginInfo('mayaCharacterization', q=True, l=True):
    cmds.loadPlugin('mayaCharacterization')
    if not cmds.pluginInfo('retargeterNodes', q=True, l=True):
    cmds.loadPlugin('retargeterNodes')

PLAYBLASTER_PATH = '.mb'
