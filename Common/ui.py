#local app packages
import maya.cmds as mc
#from Qt import QtWidgets, QtGui, QtCore

import os
from functools import partial
from PySide2 import QtCore, QtGui, QtWidgets, QtUiTools


class UI(object):
    def __init__(self, ui_file=None):
        super(UI, self).__init__()
        ui_file = QtCore.QFile(ui_file)
        ui_file.open(QtCore.QFile.ReadOnly)

        loader = QtUiTools.QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()
        self.__init__widgets()

    def __init__widgets(self):
        print ('initialize common.ui')
        #self.line = self.window.findChild(QtWidgets.QLineEdit, 'lineEdit')
        #self.button = self.window.findChild(QtWidgets.QPushButton, 'pushButton')
        #self.button.pressed.connect(partial(self.print_button_label))

    def print_button_label(self):
        print (self.button.text())


