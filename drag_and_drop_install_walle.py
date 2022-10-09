"""
Drag and drop this file into your viewport to run the installer.
NEED TO BE OUTSIDE WALLE TO BE USED PROPERLY
"""

import sys
import os
import glob
import shutil
import stat
import traceback
import time
import maya.cmds as mc
import maya.mel as mel
#mport pymel.core as pm
import pathlib
# Next update just use pathlib :)

srcPath = pathlib.Path(__file__).parent
shared_command = f'''
import os
import sys
    
if not os.path.exists(r'{srcPath}'):
    raise IOError(r'The source path "{srcPath}" does not exist!')
    
if r'{srcPath}' not in sys.path:
    sys.path.insert(0, r'{srcPath}')
'''

def onMayaDroppedPythonFile(*args):
    try:
        copy_scripts_to_directory()
        add_populated_shelf()

    except Exception as e:
        # Display error message if an exception was raised.
        print(traceback.format_exc())

        mc.confirmDialog(
            message=(
                "{}<br>"
                "<br>"
                "If you need help or have questions please send an e-mail with subject "
                "<b>Weights editor installation</b> to <b>jasonlabbe@gmail.com</b>".format(e)),
            title="Installation has failed!",
            icon="critical",
            button=["OK"])

def copy_scripts_to_directory():
            
        package_name = "WALLE"
        source_dir = os.path.dirname(__file__)
        source_path = os.path.normpath(os.path.join(source_dir, package_name))
        #source_path = os.path.normpath(os.path.join(source_dir, "scripts", package_name))
        
        # Make sure this installer is relative to the main tool.
        relative_path = os.path.join(source_path, "restartSessionForScript.py")
        if not os.path.exists(relative_path):
            raise RuntimeError("Unable to find 'scripts/restartSessionForScript.py' relative to this installer file.")

        # Suggest to install in user's script preferences.
        prefs_dir = os.path.dirname(mc.about(preferences=True))
        scripts_dir = os.path.normpath(os.path.join(prefs_dir, "scripts"))

        continue_option = "Continue"
        manual_option = "No, let me choose"
        cancel_option = "Cancel"

        dialog = mc.confirmDialog(
            message=(
                "WALLE will be installed in a new folder here:<br>"
                "<i>{}</i>".format(os.path.normpath(os.path.join(scripts_dir, package_name)))),
            title="Installation path", icon="warning",
            button=[continue_option, manual_option, cancel_option],
            cancelButton=cancel_option, dismissString=cancel_option)

        if dialog == continue_option:
            install_path = scripts_dir
        elif dialog == manual_option:
            install_path = None
        else:
            return
        
        # Open file picker to choose where to install to.
        if install_path is None:
            results = mc.fileDialog2(
                fileMode=3,
                okCaption="Install here",
                caption="Pick a folder to install to",
                dir=scripts_dir)
            
            # Exit if it was cancelled.
            if not results:
                return
            
            install_path = os.path.normpath(results[0])
        
        # Check if install path is in Python's path.
        python_paths = [os.path.normpath(path) for path in sys.path]
        if install_path not in python_paths:
            cancel_option = "Cancel"

            dialog = mc.confirmDialog(
                message=(
                    "Uh oh! Python can't see the path you picked:<br>"
                    "<i>{}</i><br><br>"
                    "This means the tool won't run unless you add this path to your environment variables using <b>Maya.env</b> or <b>userSetup.py</b>."
                    "<br><br>"
                    "Would you like to continue anyways?".format(install_path)),
                title="Path not found in Python's paths!", icon="warning",
                button=["Continue", cancel_option],
                cancelButton=cancel_option, dismissString=cancel_option)
            
            if dialog == cancel_option:
                return

        # If it already exists, asks if it's ok to overwrite.
        tool_path = os.path.join(install_path, package_name)
        if os.path.exists(tool_path):
            dialog = mc.confirmDialog(
                message=(
                    "This folder already exists:<br>"
                    "<i>{}</i><br><br>"
                    "Continue to overwrite it?".format(tool_path)),
                title="Warning!", icon="warning",
                button=["OK", "Cancel"],
                cancelButton="Cancel", dismissString="Cancel")
            
            if dialog == "Cancel":
                return

            # May need to tweak permissions before deleting.
            for root, dirs, files in os.walk(tool_path, topdown=False):
                for name in files + dirs:
                    os.chmod(os.path.join(root, name), stat.S_IWUSR)

            shutil.rmtree(tool_path)
        
        # Windows may throw an 'access denied' exception doing a copytree right after a rmtree.
        # Forcing it a slight delay seems to solve it.
        time.sleep(1)
        
        # Copy tool's directory over.
        shutil.copytree(source_path, tool_path)

        # Display success!
        mc.confirmDialog(
            message=(
                "The tool has been successfully installed!<br><br>"
                "If you want to remove it then simply delete this folder:<br>"
                "<i>{}</i><br><br>"
                "Run the tool from the script editor by executing the following:<br>"
                "<b>-------<br>"
                "------</b>".format(tool_path)),
            title="Install successful!",
            button=["OK"])
        ''''''

def add_populated_shelf():
    create_shelf()
    #add individual items
    print('running populated shelf---------')
    add_shot_creator_as_shelf_item()
    add_shot_browser_as_shelf_item()
    add_asset_creator_as_shelf_item()
    add_asset_publisher_as_shelf_item()
    add_asset_loader_as_shelf_item()
    add_attribute_anim_as_shelf_item()
    add_megascan_loader_as_shelf_item()




def add_shot_creator_as_shelf_item():
            ### shot creator ###
    srcPath = pathlib.Path(__file__).parent
    iconPath = _get_icon_path_helper('I_shotCreator.png')
    item_command = f'''    
import WALLE.SceneManagement.scene_creator as sc
import imp
imp.reload(sc)

sc_window = sc.create_shot_creator_window()
sc_window.show()
    '''
    command = shared_command + item_command
    annotation = 'widget for creating shot and puts in the corresponding directory'
    shot_creator = Shelf_Item(srcPath,iconPath,command,annotation)
    shot_creator.create_shelf_item()

def add_shot_browser_as_shelf_item():
            ### shot creator ###
    #srcPath = pathlib.Path(__file__).parent
    iconPath = _get_icon_path_helper('I_shotBrowser.png')
    item_command = f'''    
import WALLE.SceneManagement.shot_browser as sc
import imp
imp.reload(sc)

sc_window = sc.main()
sc_window.show()
    '''
    command = shared_command + item_command
    annotation = 'widget for browsing shots'
    shelf_item_instance = Shelf_Item(srcPath,iconPath,command,annotation)
    shelf_item_instance.create_shelf_item()

def add_asset_creator_as_shelf_item():
            ### shot creator ###
    #srcPath = pathlib.Path(__file__).parent
    iconPath = _get_icon_path_helper('I_assetCreator.png')
    item_command = f'''    
import WALLE.SceneManagement.scene_creator as sc
import imp
imp.reload(sc)

asset_window = sc.create_asset_creator_window()
asset_window.show()
    '''
    command = shared_command + item_command
    annotation = 'widget for creating maya file for assets'
    shelf_item_instance = Shelf_Item(srcPath,iconPath,command,annotation)
    shelf_item_instance.create_shelf_item()

def add_asset_publisher_as_shelf_item():
            ### shot creator ###
    #srcPath = pathlib.Path(__file__).parent
    iconPath = _get_icon_path_helper('I_assetPublisher.png')
    item_command = f'''    
import WALLE.SceneManagement.scene_creator as sc
import imp
imp.reload(sc)

asset_window = sc.publish_asset_creator_window()
asset_window.show()
    '''
    command = shared_command + item_command
    annotation = 'widget for publishing the asset as fbx and maya file'
    shelf_item_instance = Shelf_Item(srcPath,iconPath,command,annotation)
    shelf_item_instance.create_shelf_item()

def add_asset_loader_as_shelf_item():
            ### shot creator ###
    #srcPath = pathlib.Path(__file__).parent
    iconPath = _get_icon_path_helper('I_assetLoader.png')
    item_command = f'''    
import WALLE.SceneManagement.scene_creator as sc
import imp
imp.reload(sc)

asset_window = sc.asset_loader_creator_window()
asset_window.show()

    '''
    command = shared_command + item_command
    annotation = 'widget for loading in publisehd assets'
    shelf_item_instance = Shelf_Item(srcPath,iconPath,command,annotation)
    shelf_item_instance.create_shelf_item()

def add_megascan_loader_as_shelf_item():

    iconPath = _get_icon_path_helper('I_megascanLoader.png')
    item_command = f'''    
import WALLE.SceneManagement.scene_creator as sc
import imp
imp.reload(sc)

megascan_window = sc.megascan_loader_creator_window()
megascan_window.show()

    '''
    command = shared_command + item_command
    annotation = 'widget for loading in megascan assets'
    shelf_item_instance = Shelf_Item(srcPath,iconPath,command,annotation)
    shelf_item_instance.create_shelf_item()

def add_attribute_anim_as_shelf_item():
            ### shot creator ###
    #srcPath = pathlib.Path(__file__).parent
    iconPath = _get_icon_path_helper('I_attributeAnimation.png')
    item_command = f'''    
import WALLE.Animation.AttributeAnimation as anim
anim_window = anim.main()
anim_window.show()
    '''
    command = shared_command + item_command
    annotation = 'widget for attribute animation'
    shelf_item_instance = Shelf_Item(srcPath,iconPath,command,annotation)
    shelf_item_instance.create_shelf_item()



def _get_icon_path_helper(icon_name):
    return pathlib.Path(pathlib.PurePath(srcPath, 'WALLE/Icons', icon_name))


def create_shelf():
    
    ### This part creates the Walle_tools shelf ###
    print('creating shelf')
    parentShelf = mel.eval('$gShelfTopLevel=$gShelfTopLevel')
    currentShelves = mc.tabLayout(parentShelf,query=1,childArray=1)
    

    walle_tool = False
    for shelf in currentShelves:
        if 'Walle_tools' in shelf:
            walle_tool = True
            items = mc.shelfLayout(shelf,query=1,childArray=1)
            if items != None:
                for i in items:
                    
                    mc.deleteUI(i) # deletes walle_tool shelf and all contents
                    print('Walle_tools shelf tools removed for re-install')
    if not walle_tool:
        mel.eval('addNewShelfTab "Walle_tools";')
        print('New Walle_tools shelf made!') # makes Walle_tools shelf

    ### This part creates the shelf items ###
    ### All packaged into an easy to use class ###

class Shelf_Item():
    ''' 
    Shelf Item Object Class
    Makes it quick and easy to add new shelf item
    '''
    def __init__(self, source, icon, command, annotation, parent = mel.eval('$gShelfTopLevel=$gShelfTopLevel'), noDefaultPopup = False) -> None:
        self.source= pathlib.Path(source)
        self.icon = pathlib.Path(icon)
        self.command = command
        self.annotation = annotation
        self.parent = mc.tabLayout(parent, query=True, selectTab=True)
        self.noDefaultPopup = noDefaultPopup

    def create_shelf_item(self):
        ''' Creates Shelf Item '''

        if not pathlib.Path.exists(self.source):
            raise IOError('Cannot find ' + str(self.source))

        if not pathlib.Path.exists(self.icon):
            raise IOError('Cannot find ' + str(self.icon))

        srcPath = str(self.source)
        iconPath = str(self.icon)
        
        #check if shelve contains it ??
        items = mc.shelfLayout(self.parent,query=1,childArray=1)


        shelfButton = mc.shelfButton(
            command = self.command,
            annotation = self.annotation,
            sourceType = 'Python',
            image = self.icon,
            image1 = self.icon,
            parent = self.parent,
            noDefaultPopup = self.noDefaultPopup
        )

        return shelfButton