from importlib.resources import path
import os
import shutil
import maya.cmds as mc
from PySide2 import QtWidgets, QtGui, QtCore

#delete a directory including its sub contents! use with caution
def delete_directory(dir_path):    
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))


#icon utils
def set_icon(qLabel, icon_name):
    icon_path = get_icon_path(icon_name)
    qLabel.pixmap().load(icon_path)

def get_icon_path(icon_name):
    script_folder=get_script_folder_location()
    icon_path = script_folder+'/WALLE/icons/'+icon_name
    return icon_path



'''
inputs: file path (relatively to work space), 
outputs: a list of directories
goal: used to populate folder 
'''

def list_directories_from_path(relative_path_in):
    root_dir = mc.workspace(q=True, rd=True)
    full_path = root_dir + relative_path_in
    if os.path.exists(full_path):
        dirs_and_files = os.listdir(full_path)
        filtered_dirs = []

        for item in dirs_and_files:
            if '.' not in item:   
                filtered_dirs.append(item)
                    #self.window.cmb_sequence.addItem(str(seq))
        return filtered_dirs
    return None


def populate_combo_box_from_dirs(combobox, path_in):
    combobox.clear()

    dir_list = list_directories_from_path(path_in)
    
    if (dir_list):
        for dir in dir_list:
            combobox.addItem(str(dir))
    else:
        print('empty list')



'''
inputs: file path (relatively to work space), 
outputs: a map of recursive files, key being their short name and value being their full path
goal: used to populate folder 
'''
def list_files_from_path(path_in):
    
    print('this is the list: ')

#returns what the maya/script directory is
#C:/Users/ymz19/Documents/maya/2022/scripts
def get_script_folder_location():
    script_location = __file__
    find_index = script_location.find('scripts')
    script_folder = script_location[:find_index+7]
    print('get script folder location: '+script_folder)
    return script_folder

