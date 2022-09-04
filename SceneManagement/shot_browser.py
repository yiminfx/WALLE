import os
import maya.cmds as mc

#local
import WALLE.Common.ui as commonUI

from functools import partial

ROOT_NAME = "ROOT"

class MayaShotBrowser(commonUI.UI):
    _obj_name = "shot_browser"
    _window_title = "Shot Browser"
    fullpath = None
    files_dict={}


    def __init__(self, ui_file=None):
        print('initalizing...ui file is '+ ui_file)
        super().__init__(ui_file)

    def _post_ui_setup(self):    
        #self.window.btn_create.clicked.connect(partial(self.create_shot_from_input))
        self.window.btn_open_shot.clicked.connect(partial(self.open_shot))

        self.assign_widgets()
        self._populate_sequence()

        

        #self._populate_shots()
        #self.options.btn_open_scene.clicked.connect(self.cb_open_scene_clicked)
        print('')

    def build_tree(self):
        '''
        finds all the maps and build the model tree with map keys
        returns root_node (context tree) the tree root node

        '''
        print('')
        #self.root_node = mdl.ContextTreeNode(name = ROOT_NAME)
    
    def assign_widgets(self):
        print('assigning widgets')
        self.window.lst_sequence.itemSelectionChanged.connect(partial(self._populate_shots))
        self.window.lst_shots.itemSelectionChanged.connect(partial(self._populate_files))
        #self.window.lst_sequence.currentItemChanged.connect(partial(self._populate_shots))
        #self.window.lst_sequence.currentItemChanged.connect(self._populate_shots)

    def _populate_sequence(self):
        

 
        self.window.lst_sequence.clear()

        root_dir = mc.workspace(q=True, rd=True)
        seq_dir = root_dir+"shots"
    
        seqDirs = os.listdir(seq_dir)

        for seq in seqDirs:
            if '.' not in seq:
                self.window.lst_sequence.addItem(str(seq))
                #self.window.cmb_sequence.addItem(str(seq))

        if (seqDirs):
            self.window.lst_sequence.setItemSelected(self.window.lst_sequence.item(0), True)
        

    def _populate_shots(self):
        print('populating shot')
        self.window.lst_shots.clear()

        root_dir = mc.workspace(q=True, rd=True)
        current_seq=self.window.lst_sequence.selectedItems()[0].text()
        #print('current sequence is ' + str(current_seq))

        seq_dir = root_dir+"shots"+'/'+ current_seq
        shot_dirs = os.listdir(seq_dir)
        for shot in shot_dirs:
            if '.' not in shot:
                self.window.lst_shots.addItem(str(shot))

        if (shot_dirs):
            self.window.lst_shots.setItemSelected(self.window.lst_shots.item(0), True)

   
    def open_shot(self):
        if(self.window.lst_files.selectedItems):
            current_file= self.window.lst_files.selectedItems()[0].text()

            if (current_file):
                full_path=self.files_dict[current_file]
                print(self.files_dict[current_file])
                mc.file(new=True, force=True)# for runtime unsaved changes error
                mc.file(full_path, o=True)

        else:
            print ('no files listed!')


    def _populate_files(self):
        print('populating files')
        self.window.lst_files.clear()

        root_dir = mc.workspace(q=True, rd=True)
        current_seq=self.window.lst_sequence.selectedItems()[0].text()
        current_shot = self.window.lst_shots.selectedItems()[0].text()

        shot_dir = root_dir+"shots"+'/'+ current_seq + '/' + current_shot

        file_dirs = os.listdir(shot_dir)
        mFiles= []
        rootdir = shot_dir
        self.files_dict.clear()

        for rootdir, dirs, files in os.walk(rootdir):
            for n in range(0, len(files)):
                #if ((MustHaveStrings=="") or (files[n].find(MustHaveStrings) != -1)):
                #hisFile = (root.replace("\\", "/")) + "/" + (files[n])
                mFiles.append(files[n])
                path = os.path.join(rootdir, files[n])
                path = path.replace("\\", "/")
                print (path)
                self.files_dict[files[n]]= path

           # for subdir in dirs:
                #print(os.path.join(rootdir, subdir))
               # print (file=)

 
        for m in mFiles:
            self.window.lst_files.addItem(str(m))
        
        if (mFiles[0]):
            self.window.lst_files.setItemSelected(self.window.lst_files.item(0), True)



        '''
        for mFile in file_dirs:
            #print (mFile)
            if '_' in mFile:
                self.window.lst_files.addItem(str(mFile))
        '''





        





    




        



def main():

    # 'C:\Users\colton\Documents\maya\scripts\week6\designerInterface\\friendsListInterface.ui'
    parentDir = os.path.split(__file__)[0]
    #parentDir = 'C:\Users\ymz19\Documents\maya\\2020\scripts\WALLE\Animation'
    uiFilePath = os.path.join(parentDir, 'shot_browser.ui')

    print(uiFilePath)

    sc_window= MayaShotBrowser(ui_file=uiFilePath)
    sc_window._post_ui_setup()

    return sc_window.window

'''
import WALLE.SceneManagement.scene_creator as sc
import imp
imp.reload(sc)

sc_window = sc.main()
sc_window.show()


main()
'''
