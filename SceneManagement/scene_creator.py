from functools import partial
import os


#local app packages
import maya.cmds as mc
import maya.mel as mel
import pymel.core as pm


#from PySide import QtCore
#from PySide import QtGui
#local
import WALLE.Common.ui as commonUI
import WALLE.Utils.path_utils as path_utils
import imp
imp.reload(path_utils)



class scene_factory(object):
    def __init__(self, file_path, create_from, background):
        self.file_path = file_path
        self.create_from = create_from
        self.background = background
        self.output_path = self.file_path
        self.version_num = 1
        self.file_name = 'default'
        
    def import_maya_file(self):
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
        self.formatted_version = str(self.version_num).rjust(3, '0')
  
        #self.file_name = self.sequence+ "_" + self.shot_num + "_" + self.task + "_v" + str(formatted_version)
        self.file_name = self.asset_type + '_' + self.asset_subtype + '_' + self.asset_name + '_' + self.asset_variation + '_v'+ self.formatted_version
        

    def create_asset(self, task='create', is_publish=False):
        root_dir = mc.workspace(q=True, rd=True)
        self.output_path = root_dir + 'assets' + "/" + self.asset_type + "/" + self.asset_subtype +'/'+self.asset_name+ "/" + self.asset_variation 

        if (task=='create'):
            wip_path = self.output_path+"/wip/maya/" +self.file_name 
            self.save_maya_file_as()

        if (task=='publish'):
            fbx_path = self.output_path + '/pub/engine/' +self.file_name
            ma_path = self.output_path + "/pub/maya/" +self.file_name

            #export fbx here
            self.output_path= fbx_path
            self.save_maya_file_as(export_as_ref=True,type_fbx=True)

            #export regular maya file here
            self.output_path= ma_path
            self.save_maya_file_as(export_as_ref=False,type_fbx=False)

            #print('creating asset')
            #print(self.output_path)
        if (task=='load'):
            ma_path = self.output_path + "/pub/maya/" +self.file_name
            self.output_path= ma_path +'.ma'
            print('path is ' + ma_path)

            self.import_maya_file()


            print('this is loading working')

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
        self._popualte_sub_type()

    def assign_widgets(self):
        self.window.cmb_asset_type.editTextChanged.connect(self._popualte_sub_type)
        self.window.cmb_asset_type.currentIndexChanged.connect(self._popualte_sub_type)
        self.window.cmb_subtype.editTextChanged.connect(self._populate_asset_name)
        self.window.cmb_subtype.currentIndexChanged.connect(self._populate_asset_name)
        self.window.cmb_asset_name.editTextChanged.connect(self._populate_asset_variation)
        self.window.cmb_asset_name.currentIndexChanged.connect(self._populate_asset_variation)



    def _popualte_sub_type(self):
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
        
    #     self.window.cmb_asset_type.editTextChanged.connect(self._popualte_sub_type)
    #     self.window.cmb_asset_type.currentIndexChanged.connect(self._popualte_sub_type)
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
        #self.window.close()




class asset_loader_window(asset_creator_window):
    _object_name= 'asset_loader_window'
    _window_title = 'Asset Loader'
    

    def __init__(self, ui_file=None):
        #print('initalizing...ui file is '+ ui_file)
        super().__init__(ui_file)
        self._post_ui_setup()


    def _post_ui_setup(self):
        self.window.btn_load_asset.clicked.connect(partial(self.load_asset))
        self.assign_widgets()
        path_utils.set_icon(self.window.lbl_icon, 'i_assetLoader.png')
        self._popualte_sub_type()
    
    # def assign_widgets(self):
        
    #     self.window.cmb_asset_type.editTextChanged.connect(self._popualte_sub_type)
    #     self.window.cmb_asset_type.currentIndexChanged.connect(self._popualte_sub_type)
    def load_asset(self):
        self._create_asset_from_input('load')

        # asset_type = self.window.cmb_asset_type.currentText()
        # asset_subtype= self.window.cmb_subtype.currentText()
        # asset_name= self.window.cmb_asset_name.currentText()
        # asset_variation = self.window.cmb_variation.currentText()
        # #suffix = self.window.cmb_suffix.currentText()


        # if(asset_type):
        #     if(asset_subtype):
        #         if(asset_name):
        #             if (asset_variation):
        #                 my_asset_creator= asset_creator(asset_type, asset_name, asset_variation, subtype=asset_subtype)
        #                 #TODO:unhide here
        #                 #my_asset_creator.create_asset('load')
                        
   









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


