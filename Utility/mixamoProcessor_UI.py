from functools import partial
from PySide2 import QtWidgets, QtGui, QtCore
import maya.cmds as mc

from WALLE.Utility import mixamoProcessor as mp 
reload(mp)

class UI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(UI, self).__init__(parent)
        self.folderpath=None
        self.exportFolderPath=None

        self.setWindowTitle('Add Root To Mixamo Animations')
        self._init_widgets()
        self._init_layout()
        self.setCentralWidget(self.centralWidget)
        self.setLayout(self.mainLayout)

    def _init_widgets(self):
        self.centralWidget = QtWidgets.QGroupBox('Choose animations to convert from and to :', self)
        self.label_folder_anim = QtWidgets.QLabel('anim folder not selected')
        self.label_folder_export = QtWidgets.QLabel('export folder not selected')
        self.combo = QtWidgets.QComboBox()
        self.combo.addItem('Red')

        self.button = QtWidgets.QPushButton('Browse Animation Folder')
        self.button.setToolTip('This will browse the animation')
        self.button.pressed.connect(self.browse_anim_pressed)
        
        self.btn_setExport =  QtWidgets.QPushButton('Browse Export Folder')
        self.btn_setExport.pressed.connect(self.browse_export_pressed)
        
        self.btn_executeExport =  QtWidgets.QPushButton('Export')
        self.btn_executeExport.pressed.connect(self.execute_export_pressed)
        self.btn_executeExport.setStyleSheet("background-color : #166ebf")

        self.btn_executeExport.setMaximumWidth(200)
        self.btn_executeExport.setMinimumWidth(180)
        
        self.btn_executeExport.setMaximumHeight(50)
        self.btn_executeExport.setMinimumHeight(40)
        
        
        self.originalColor = self.button.palette().color(self.button.backgroundRole())
        self.textColor = self.button.palette().color(self.button.foregroundRole())

        # signals
        #self.combo.activated.connect(self.set_button_color)

    def _init_layout(self):
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        #self.mainLayout.addWidget(self.combo)
        
        self.mainLayout.addWidget(self.label_folder_anim)
        self.mainLayout.addWidget(self.button)
        self.mainLayout.addWidget(self.label_folder_export)

        self.mainLayout.addWidget(self.btn_setExport)
        self.mainLayout.addWidget(self.btn_executeExport)
        
        
        
    def browse_anim_pressed(self):
        self.folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder for animations')
        self.label_folder_anim.setText(self.folderpath)
    
    def browse_export_pressed(self):
        self.exportFolderPath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder to export')
        self.label_folder_export.setText(self.exportFolderPath)
        
    def execute_export_pressed(self):
        print("excuting export")
        if (self.folderpath and self.exportFolderPath):
            mp.convert_mxm_animations(self.folderpath,self.exportFolderPath)
        else:
             mc.warning('please set the 2 folder paths first')
            


        
        
def main():
    my_app = UI()
    my_app.show()
    return my_app
    
ui = main()
 