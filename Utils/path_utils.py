from importlib.resources import path
import os
import pathlib
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
returns the path of the image
'''
def get_asset_capture_path(relative_path):
    files_dict = list_files_from_path(relative_path)
    print('getting asset capture path')
    image_path = ''
    for key in files_dict:
        if '.jpg' in key:
            image_path = files_dict[key]
            #print('searching through file for capture ' + key)
    
    return image_path

def get_user_document_folder():
    return os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')


'''
inputs: file path (relatively to work space), 
outputs: a list of directories
goal: used to populate folder 
'''
def list_directories_from_path(relative_path_in):
    root_dir = mc.workspace(q=True, rd=True)
    full_path = root_dir + relative_path_in
    return _list_directories_from_path_absolute(full_path)

def _list_directories_from_path_absolute(abs_path):
    if os.path.exists(abs_path):
        dirs_and_files = os.listdir(abs_path)
        filtered_dirs = []

        for item in dirs_and_files:
            if '.' not in item:   
                filtered_dirs.append(item)
                    #self.window.cmb_sequence.addItem(str(seq))
        return filtered_dirs
    return None
'''
adds items in a directory to a combobox
'''
def populate_combo_box_from_dirs(combobox, path_in, relative_path=True):
    combobox.clear()

    if (relative_path):
        dir_list = list_directories_from_path(path_in)
    else:
        dir_list = _list_directories_from_path_absolute(path_in)
    
    if (dir_list):
        for dir in dir_list:
            #print('a')
            combobox.addItem(str(dir))
    else:
        print('empty list - populate combo box from dirs')




'''
inputs: file path (relatively to work space), 
outputs: a map of recursive files, key being their short name and value being their full path
goal: used to populate folder 
'''
def list_files_from_path(path_in):
    
    root_dir = mc.workspace(q=True, rd=True)
    asset_dir = root_dir + path_in
    #return _list_directories_from_path_absolute(asset_dir)
    file_dirs = os.listdir(asset_dir)
    mFiles= []
    
    rootdir = asset_dir
    files_dict={}
    #files_dict.clear()

    for rootdir, dirs, files in os.walk(rootdir):
        for n in range(0, len(files)):
            #if ((MustHaveStrings=="") or (files[n].find(MustHaveStrings) != -1)):
            #hisFile = (root.replace("\\", "/")) + "/" + (files[n])
            mFiles.append(files[n])
            path = os.path.join(rootdir, files[n])
            path = path.replace("\\", "/")
            #print ('listing file from path ' + path)
            files_dict[files[n]]= path
    return files_dict


def _list_files_from_path_abs_nonrecursive(abs_path):
    if os.path.exists(abs_path):
        dirs_and_files = os.listdir(abs_path)
        filtered_dirs = []

        for item in dirs_and_files:
            #if '.' in item:   
            filtered_dirs.append(item)
                    #self.window.cmb_sequence.addItem(str(seq))
        return filtered_dirs
    return None

def _list_files_from_path_abs(path_abs):
    
    file_dirs = os.listdir(path_abs)
    mFiles= []

    rootdir = path_abs
    files_dict={}
    #files_dict.clear()

    for rootdir, dirs, files in os.walk(rootdir):
        for n in range(0, len(files)):
            #if ((MustHaveStrings=="") or (files[n].find(MustHaveStrings) != -1)):
            #hisFile = (root.replace("\\", "/")) + "/" + (files[n])
            mFiles.append(files[n])
            path = os.path.join(rootdir, files[n])
            path = path.replace("\\", "/")
            print('listing files from path abs')
            print (path)
            files_dict[files[n]]= path
    return files_dict
#returns what the maya/script directory is
#C:/Users/ymz19/Documents/maya/2022/scripts
def get_script_folder_location():
    script_location = pathlib.Path(__file__).parent.parent.parent
    print('script location is ' + script_location.__str__())
    return script_location.__str__()

