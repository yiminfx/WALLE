from functools import partial
from importlib.resources import path
import json
import os


#local app packages
import maya.cmds as mc
import maya.mel as mel


#from PySide import QtCore
from PySide2 import QtGui
#local
import WALLE.Common.ui as commonUI
import WALLE.Common.dependencies as dependencies
import WALLE.Utils.path_utils as path_utils
import WALLE.Utils.capture_utils as capture_utils

import imp
imp.reload(path_utils)
imp.reload(capture_utils)
imp.reload(commonUI)
imp.reload(dependencies)


class scene_factory(object):
    def __init__(self, file_path, create_from, background):
        self.file_path = file_path
        self.create_from = create_from
        self.background = background
        self.output_path = self.file_path
        self.version_num = 1
        self.file_name = 'default'
        
    def import_maya_file(self, reference=False):
        if(reference):
            mc.file(self.output_path, r=True)
        else:
            mc.file(self.output_path, i=True)
        
        
    #save the current maya file to the output path
    def save_maya_file_as(self, export_as_ref=False, type_fbx=False):

        shot_directory=os.path.dirname(self.output_path)
        
        if not os.path.exists(shot_directory):
            os.makedirs(shot_directory)

        mc.file(rename=self.output_path)
        if (export_as_ref):
            if(type_fbx):
                #c.file(force=True, type="OBJexport", pr=True, es=True)
                mc.file(force=True, type='FBX export', pr=True, exportAll=True)
                # Export the given fbx filename
                # mel.eval('FBXResetExport')
                # mel.eval('FBXExportBakeComplexAnimation -v 1')
                # mel.eval('FBXExportInAscii -v 1')
                # mel.eval(('FBXExport -f \"{}\" -s').format(self.file_name))
            else:
                mc.file(save=True, type="mayaAscii", exportAsReference=True)

        else:
            mc.file(save=True, type="mayaAscii")

    
#creator is used to make the asset. initialize it to fill the info
class asset_creator(scene_factory):
    def __init__(self, asset_type, asset_name, asset_variation, file_path='', create_from='', background='', output_path='', subtype=None):
        scene_factory.__init__(self, file_path, create_from, background)
        print('initiating a asset creator')
        self.asset_type = asset_type
        self.asset_name = asset_name
        self.asset_subtype = subtype
        self.asset_variation = asset_variation
        self.capture_path = None
        self.formatted_version = str(self.version_num).rjust(3, '0')
  
        #self.file_name = self.sequence+ "_" + self.shot_num + "_" + self.task + "_v" + str(formatted_version)
        self.file_name = self.asset_type + '_' + self.asset_subtype + '_' + self.asset_name + '_' + self.asset_variation + '_v'+ self.formatted_version
    
    def get_output_path(self):
        root_dir = mc.workspace(q=True, rd=True)
        self.output_path = root_dir + 'assets' + "/" + self.asset_type + "/" + self.asset_subtype +'/'+self.asset_name+ "/" + self.asset_variation 
        return self.output_path

    def get_output_texture_path(self):
        self.get_output_path()
        tex_path = self.output_path + "/pub/textures"
        if not os.path.exists(tex_path):
            os.makedirs(tex_path)
        return tex_path
    #this method will create fbx file or maya file depends on if the task is create or publish
    def create_asset(self, task='create', is_publish=False):
        root_dir = mc.workspace(q=True, rd=True)
        self.output_path = root_dir + 'assets' + "/" + self.asset_type + "/" + self.asset_subtype +'/'+self.asset_name+ "/" + self.asset_variation 

        if (task=='create'):
            wip_path = self.output_path+"/wip/maya/" +self.file_name 
            self.save_maya_file_as()

        if (task=='publish'):
            fbx_path = self.output_path + '/pub/engine/' +self.file_name
            ma_path = self.output_path + "/pub/maya/" +self.file_name
            capture_dir = self.output_path + "/pub/capture"

            
            #export fbx here
            self.output_path= fbx_path
            self.save_maya_file_as(export_as_ref=True,type_fbx=True)

            #export regular maya file here
            self.output_path= ma_path
            self.save_maya_file_as(export_as_ref=False,type_fbx=False)

            #export capture
            capture_utils.saveScreenshot(self.file_name,capture_dir)

            #print('creating asset')
            #print(self.output_path)
        if (task=='load'):
            ma_path = self.output_path + "/pub/maya/" +self.file_name
            self.output_path= ma_path +'.ma'
            print('loading path is ' + ma_path)
            self.import_maya_file()
        if (task=='ref'):
            ma_path = self.output_path + "/pub/maya/" +self.file_name
            self.output_path= ma_path +'.ma'
            print('loading path is ' + ma_path)
            self.import_maya_file(reference=True)


class shot_creator(scene_factory):
    def __init__(self, sequence, shot_num, vis_step="", task="", set_timeline="", start_frame="", end_frame="", file_path="", create_from="", background="", output_path="", skip_maya="", suffix=""):
        scene_factory.__init__(self, file_path, create_from, background)
        print('initiating a asset creator')
        self.sequence = sequence
        self.shot_num = shot_num
        self.version_num = 1
        self.task= task
        formatted_version = str(self.version_num).rjust(3, '0')
  
    
        self.file_name = self.sequence+ "_" + self.shot_num + "_" + self.task + "_v" + str(formatted_version)


        self.output_path = self.file_path
   
    def create_shot(self):        
       
        root_dir = mc.workspace(q=True, rd=True)
        #if the directory doesnt exist, create it
        self.output_path = root_dir+"shots"+ "/" + self.sequence + "/"+ self.shot_num +"/" + self.task + "/"+ self.file_name
        self.save_maya_file_as()



class asset_creator_window(commonUI.UI):
    _object_name= 'attribute_animation_window'
    _window_title = 'Attribute Animation'
    
    def __init__(self, ui_file=None):
        
        super().__init__(ui_file)
        self._post_ui_setup()


    def _post_ui_setup(self):
        self.window.btn_create_asset.clicked.connect(partial(self.create_asset_from_input))

        #icon_path = 'C:/Users/ymz19/Documents/maya/2022/scripts/WALLE/Icons/i_assetCreator.png'
        #icon_path = path_utils.get_icon_path('i_assetCreator.png')
        path_utils.set_icon(self.window.lbl_icon, 'i_assetCreator.png')
        #pixmap = QtGui.QPixmap('i_assetCreator.png')
        #self.window.lbl_icon.setPixmap()
        #path_utils.populate_combo_box_from_dirs(self.window.cmb_asset_type, 'assets')
        self.assign_widgets()
        self._populate_sub_type()

    def assign_widgets(self):
        self.window.cmb_asset_type.editTextChanged.connect(self._populate_sub_type)
        #self.window.cmb_asset_type.currentIndexChanged.connect(self._populate_sub_type)
        self.window.cmb_subtype.editTextChanged.connect(self._populate_asset_name)
        #self.window.cmb_subtype.currentIndexChanged.connect(self._populate_asset_name)
        self.window.cmb_asset_name.editTextChanged.connect(self._populate_asset_variation)
        #self.window.cmb_asset_name.currentIndexChanged.connect(self._populate_asset_variation)
        #update image
        if (self.window.cmb_variation):
            self.window.cmb_variation.currentIndexChanged.connect(self._populate_variation_capture)

    def grab_dependencies(self, tex_dir):
        file_dependencies = dependencies.FileDependencies()
        file_dependencies.get_file_textures()
        #path = 'C:/Users/ymz19/Documents/maya/projects/default/assets/char/girl/pessantGirl/base6/pub'
        file_dependencies.move_textures(custom_path=tex_dir)
        

    def _populate_variation_capture(self):
        print('running populate variation capture')
        capture_path=None
        variation_path = 'assets/'+ self.window.cmb_asset_type.currentText()+'/'+self.window.cmb_subtype.currentText() +'/' + self.window.cmb_asset_name.currentText() + '/' +self.window.cmb_variation.currentText()
        img_path = path_utils.get_asset_capture_path(variation_path)
        #setting it to default icon
        if not img_path:
            img_path = path_utils.get_icon_path('i_assetLoader.png')
        pixmap= QtGui.QPixmap(img_path)
        self.window.lbl_icon.setPixmap(pixmap)

        #print('variation')

    def _populate_sub_type(self):
        #print('www')
        path_utils.populate_combo_box_from_dirs(self.window.cmb_subtype, 'assets/'+ self.window.cmb_asset_type.currentText())
    
    def _populate_asset_name(self):
        asset_path = 'assets/'+ self.window.cmb_asset_type.currentText()+'/'+self.window.cmb_subtype.currentText()
        path_utils.populate_combo_box_from_dirs(self.window.cmb_asset_name, asset_path)
    
    def _populate_asset_variation(self):
        
        asset_path = 'assets/'+ self.window.cmb_asset_type.currentText()+'/'+self.window.cmb_subtype.currentText() +'/' + self.window.cmb_asset_name.currentText()
        path_utils.populate_combo_box_from_dirs(self.window.cmb_variation, asset_path)

       


    def create_asset_from_input(self):
        self._create_asset_from_input('create')


    def _create_asset_from_input(self, task='create'):
        print('creating assets')
        asset_type = self.window.cmb_asset_type.currentText()
        asset_subtype= self.window.cmb_subtype.currentText()
        asset_name= self.window.cmb_asset_name.currentText()
        asset_variation = self.window.cmb_variation.currentText()
        #suffix = self.window.cmb_suffix.currentText()


        if(asset_type):
            if(asset_subtype):
                if(asset_name):
                    if (asset_variation):
                        my_asset_creator= asset_creator(asset_type, asset_name, asset_variation, subtype=asset_subtype)
                        my_asset_creator.create_asset(task)
        #self.window.close()


class asset_publisher_window(asset_creator_window):
    _object_name= 'asset_publisher_window'
    _window_title = 'Asset publisher'
    

    def __init__(self, ui_file=None):
        print('initalizing...ui file is '+ ui_file)
        super().__init__(ui_file)
        self._post_ui_setup()


    def _post_ui_setup(self):
        self.window.btn_publish_asset.clicked.connect(partial(self.publish_asset_from_input))
        self.assign_widgets()
        
    
    # def assign_widgets(self):
        
    #     self.window.cmb_asset_type.editTextChanged.connect(self._populate_sub_type)
    #     self.window.cmb_asset_type.currentIndexChanged.connect(self._populate_sub_type)
    def create_asset_from_input(self):
        self._create_asset_from_input('publish')

    def publish_asset_from_input(self):
        print('creating assets')
        asset_type = self.window.cmb_asset_type.currentText()
        asset_subtype= self.window.cmb_subtype.currentText()
        asset_name= self.window.cmb_asset_name.currentText()
        asset_variation = self.window.cmb_variation.currentText()
        #suffix = self.window.cmb_suffix.currentText()


        if(asset_type):
            if(asset_subtype):
                if(asset_name):
                    if (asset_variation):
                        my_asset_creator= asset_creator(asset_type, asset_name, asset_variation, subtype=asset_subtype)
                        my_asset_creator.create_asset('publish')
                        tex_dir = my_asset_creator.get_output_texture_path()
                        self.grab_dependencies(tex_dir)
        #self.window.close()




class asset_loader_window(asset_creator_window):
    _object_name= 'asset_loader_window'
    _window_title = 'Asset Loader'

    def __init__(self, ui_file=None):
        #print('initalizing...ui file is '+ ui_file)
        super().__init__(ui_file)
        #self._post_ui_setup()

    def _post_ui_setup(self):
        self.window.btn_load_asset.clicked.connect(partial(self.load_asset))
        self.assign_widgets()
        path_utils.set_icon(self.window.lbl_icon, 'i_assetLoader.png')
        self._populate_sub_type()
    
    # def assign_widgets(self):
        
    #     self.window.cmb_asset_type.editTextChanged.connect(self._populate_sub_type)
    #     self.window.cmb_asset_type.currentIndexChanged.connect(self._populate_sub_type)
    def load_asset(self):
        ref_state = self.window.rdb_reference.isChecked()
        if(ref_state):
            self._create_asset_from_input('ref')
        else:
            self._create_asset_from_input('load')


    



class megascan_loader_window(asset_loader_window):
    _object_name= 'megascan_loader_window'
    _window_title = 'megascan Loader'
    
    _settings_path = os.path.join(os.getenv("HOME"), "maya", "megascan_loader_pref.json")

    document = path_utils.get_user_document_folder()
    megascan_path = ''


    def __init__(self, ui_file=None):
        #print('initalizing...ui file is '+ ui_file)
        super().__init__(ui_file)
        #self._post_ui_setup()
        
        
    def assign_widgets(self):
        print('overriding assign widget')
        self.window.cmb_asset_type.editTextChanged.connect(self._populate_sub_type)
        self.window.cmb_asset_type.currentIndexChanged.connect(self._populate_sub_type)
        self.window.cmb_subtype.currentIndexChanged.connect(self._populate_asset_LOD)
        self.window.cmb_subtype.editTextChanged.connect(self._populate_asset_LOD)

        self.window.rbt_showPref.toggled.connect(self._toggle_show_pref)
        self.window.lbl_megascanPath.setText(self.megascan_path)

        
    def _post_ui_setup(self):
        self._restore_state()
        self.window.btn_load_asset.clicked.connect(partial(self.load_asset))
        self.assign_widgets()
        path_utils.set_icon(self.window.lbl_icon, 'i_megascanLoader.png')
        self._populate_sub_type()
        self.window.gpb_pref.setVisible(False)
        self.window.btn_browse.clicked.connect(self._browse_folder)
        self.window.btn_setPref.clicked.connect(self._save_state)
        
    
    def _toggle_show_pref(self):
        print('toggle')
        state = self.window.rbt_showPref.isChecked()
        #self.window.Hbox_folderPrefs.setVisible(state)
        self.window.gpb_pref.setVisible(state)
    
    def _restore_state(self):
        """
        Restores gui's last state if the file is available.
        """
        data = self._fetch_settings()
        if(data):
            if "megascan_path" in data:
                print('data is found and setting var to ' +  data["megascan_path"])
                self.megascan_path = data["megascan_path"]
                self.window.lbl_megascanPath.setText(self.megascan_path)

        else:
             self.megascan_path=self.document+ '/Megascans Library'
             self.window.lbl_megascanPath.setText(self.megascan_path)

    def _browse_folder(self):
        
        # Open file picker to choose where to install to.
        install_path=None
        #if install_path is None:
        results = mc.fileDialog2(
            fileMode=3,
            okCaption="Install here",
            caption="Pick a folder to install to",
            #dir=scripts_dir
            )
        
        # Exit if it was cancelled.
        if not results:
            return
        
        install_path = os.path.normpath(results[0])
        self.megascan_path= os.path.normpath(results[0])
        self.window.lbl_megascanPath.setText(self.megascan_path)
    def _fetch_settings(self):
        if not os.path.exists(self._settings_path):
            return {}

        with open(self._settings_path, "r") as f:
            return json.loads(f.read())

    def _save_state(self):
        """
        Saves gui's current state to a file.
        """
        if not os.path.exists(os.path.dirname(self._settings_path)):
            os.makedirs(os.path.dirname(self._settings_path))
        
        data = {
            "megascan_path": self.megascan_path,
        }
        #OpenMaya.MGlobal.displayInfo("Saving settings to {0}".format(self._settings_path))
        
        with open(self._settings_path, "w") as f:
            f.write(json.dumps(data, indent=4, sort_keys=True))
        
        self.window.rbt_showPref.setChecked(False)
        self._toggle_show_pref()
     
    

    def _populate_sub_type(self):
        document = path_utils.get_user_document_folder()
        path_of_megascan = self.megascan_path +'/Downloaded/'+self.window.cmb_asset_type.currentText()

        path_utils.populate_combo_box_from_dirs(self.window.cmb_subtype, path_of_megascan, relative_path=False)
        #populate_combo_box_from_dirs(combobox, path_in, relative_path=True):
    def load_asset(self):
        document = path_utils.get_user_document_folder()
        path_of_megascan = self.megascan_path +'/Downloaded/'+self.window.cmb_asset_type.currentText()+ '/' + self.window.cmb_subtype.currentText() + '/'+self.window.cmb_asset_name.currentText()
        print(path_of_megascan)

        mc.file(path_of_megascan, i=True)


    def _populate_asset_LOD(self):
        self.window.cmb_asset_name.clear()
        document = path_utils.get_user_document_folder()
        path_of_megascan = self.megascan_path +'/Downloaded/'+self.window.cmb_asset_type.currentText()+ '/' + self.window.cmb_subtype.currentText()
        files_list = path_utils._list_files_from_path_abs_nonrecursive(path_of_megascan)
        print('file length is ' + str(len(files_list)))
        print(path_of_megascan)
        img_path = None
        for file in files_list:
            print(file)
            if 'LOD' in file:
                if '.fbx' in file:
                    self.window.cmb_asset_name.addItem(str(file))
                    print(file)
            if 'Preview' in file:
                if '.png' in file:
                    print('...........................')
                    img_path =path_of_megascan+'/'+file
                    print(path_of_megascan+'/'+file)

        
       
        #setting it to default icon
        if not img_path:
            img_path = path_utils.get_icon_path('i_megascanLoader.png')
        pixmap= QtGui.QPixmap(img_path).scaled(200,200)
        
        self.window.lbl_icon.setPixmap(pixmap)



    def _populate_variation_capture(self):
        capture_path=None
        variation_path = 'assets/'+ self.window.cmb_asset_type.currentText()+'/'+self.window.cmb_subtype.currentText() +'/' + self.window.cmb_asset_name.currentText() + '/' +self.window.cmb_variation.currentText()
        img_path = path_utils.get_asset_capture_path(variation_path)
        #setting it to default icon
        if not img_path:
            img_path = path_utils.get_icon_path('i_megascanLoader.png')
        pixmap= QtGui.QPixmap(img_path)
        self.window.lbl_icon.setPixmap(pixmap)


def megascan_loader_creator_window():
    parentDir = os.path.split(__file__)[0]
    uiFilePath = os.path.join(parentDir, 'megascan_loader.ui')
    asset_window= megascan_loader_window(ui_file=uiFilePath)
 
    return asset_window.window





class shot_creator_window(commonUI.UI):
    
    _object_name= 'attribute_animation_window'
    _window_title = 'Attribute Animation'
    
    def __init__(self, ui_file=None):
        print('initalizing...ui file is '+ ui_file)
        super().__init__(ui_file)


    def _post_ui_setup(self):    
        self.window.btn_create.clicked.connect(partial(self.create_shot_from_input))
        self.assign_widgets()
        self._populate_sequence()
        self._populate_shots()
        path_utils.set_icon(self.window.lbl_icon, 'i_shotCreator.png')


    def _populate_sequence(self):
        self.window.cmb_sequence.clear()
        #self.window.cmb_sequence.blockSignals(True)
        print('populating sequence')
        root_dir = mc.workspace(q=True, rd=True)
        seq_dir = root_dir+"shots"
        if not os.path.exists(seq_dir):
            os.makedirs(seq_dir)
        seqDirs = os.listdir(seq_dir)

      
        for seq in seqDirs:
            if '.' not in seq:
                self.window.cmb_sequence.addItem(str(seq))

    def _populate_shots(self):
        print('populating shots')
        self.window.cmb_shot.clear()
        root_dir = mc.workspace(q=True, rd=True)
        current_seq=self.window.cmb_sequence.currentText()
        seq_dir = root_dir+"shots"+'/'+ current_seq
        shot_dirs = os.listdir(seq_dir)
        for shot in shot_dirs:
            if '.' not in shot:
                self.window.cmb_shot.addItem(str(shot))



    def assign_widgets(self):
        self.window.cmb_sequence.editTextChanged.connect(self._populate_shots)
        self.window.cmb_sequence.currentIndexChanged.connect(self._populate_shots)





    def create_shot_from_input(self):

        print ('creating shot based on user fields')
        sequence = self.window.cmb_sequence.currentText()
        shot_num= self.window.cmb_shot.currentText()
        task= self.window.cmb_task.currentText()
        step = self.window.cmb_step.currentText()
        suffix = self.window.cmb_suffix.currentText()


        if(sequence):
            if(shot_num):
                if(task):
                    my_shot_creator= shot_creator(sequence, shot_num, step, task)
                    my_shot_creator.create_shot()
        self.window.close()


#laucn these from maya
def create_shot_creator_window():

    # 'C:\Users\colton\Documents\maya\scripts\week6\designerInterface\\friendsListInterface.ui'
    parentDir = os.path.split(__file__)[0]
    #parentDir = 'C:\Users\ymz19\Documents\maya\\2020\scripts\WALLE\Animation'
    uiFilePath = os.path.join(parentDir, 'shot_creator.ui')

    print(uiFilePath)

    sc_window= shot_creator_window(ui_file=uiFilePath)
    sc_window._post_ui_setup()

    return sc_window.window

def create_asset_creator_window():
    parentDir = os.path.split(__file__)[0]
    uiFilePath = os.path.join(parentDir, 'asset_creator.ui')
    asset_window= asset_creator_window(ui_file=uiFilePath)
    
    return asset_window.window

def publish_asset_creator_window():
    parentDir = os.path.split(__file__)[0]
    uiFilePath = os.path.join(parentDir, 'asset_publisher.ui')
    asset_window= asset_publisher_window(ui_file=uiFilePath)

    return asset_window.window

def asset_loader_creator_window():
    parentDir = os.path.split(__file__)[0]
    uiFilePath = os.path.join(parentDir, 'asset_loader.ui')
    asset_window= asset_loader_window(ui_file=uiFilePath)
 
    return asset_window.window






'''
import WALLE.SceneManagement.scene_factory as sc
import imp
imp.reload(sc)

sc_window = sc.main()
sc_window.show()


main()
'''
#my_shot_creator= shot_creator(sequence="ts2", shot_num="0320", task = "anim")
#my_shot_creator.create_shot()


