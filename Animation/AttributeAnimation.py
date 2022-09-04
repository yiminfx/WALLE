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
        print ('')
        #self.line = self.window.findChild(QtWidgets.QLineEdit, 'lineEdit')
        #self.button = self.window.findChild(QtWidgets.QPushButton, 'pushButton')
        #self.button.pressed.connect(partial(self.print_button_label))

    def print_button_label(self):
        print (self.button.text())




class AttributeAnimationWindow(UI):
    _object_name= 'attribute_animation_window'
    _window_title = 'Attribute Animation'
    
    print("creating attribute animation window")
    def _post_ui_setup(self):

        
        self.window.btn_remove.clicked.connect(partial(self.remove_objects))
        self.window.btn_add.clicked.connect(partial(self.add_objects))
        self.window.btn_useSelected.clicked.connect(partial(self.add_control))
        self.window.btn_create.clicked.connect(partial(self.create))
        self.window.btn_clear.clicked.connect(partial(self.clear))
        self.window.list_objects.itemClicked.connect(partial(self.select_objects))

        # creates a dictionary for the purpose of storing nice names and long names
        self.object_dict = {}

        #stores the control object if specified(long name)
        self.control_object = ""

        #runs startup functions to setup regexs for the text fields so you can only input valid characters
        #self.startup_functions()
    
    def startup_functions(self):
        #regex creation for names and numbers
        nameRegex = QtCore.QRegExp("([a-zA-Z])+")
        numRegex = QtCore.QregExp ("([0-9])+")

        #create validators and sets them for the text fields
        namevalidator = QtGui.QRegExpValidator(nameRegex, self.window.txt_attributename)
        self.window.txt_attributename.setValidator(namevalidator)

        startvalidator = QtGui.QRegExpValidator(numRegex, self.window.txt_startTime)
        self.window.txt_startTime.setValidator(startvalidator)

        finishvalidator = QtGui.QRegExpValidator(numRegex, self.window.text_finishTime)
        self.window.text_finishTime.setValidator(finishvalidator)

    def select_objects(self):
        objects_to_select = []
        objects_selected = self.window.list_objects.selectedItems()
        for object in objects_selected:
            objects_to_select.append(self.object_dict[object.text()])
        mc.select(objects_to_select)
    
    def clear(self):
        self.window.list_objects.clear()
        self.object_dict={}
    
    def add_objects(self):
        #1 print('adding objects')
        #1 self.dialog("adding objects.", "adding ")
        selected_objects = mc.ls(sl=1, long = True)
        for object in selected_objects:
            #if the object isnt already added
            if object not in self.object_dict.values():
                #get nice name to display for users
                object_short = object.split('|')[-1]

                #if the nice name already exist in the list, then there are duplicate node names
                #add a number after in parentheses and add that as the key to the long name or the object path
                if not self.window.list_objects.findItems(object_short, QtCore.Qt.MatchExactly):
                    self.window.list_objects.addItem (object_short)
                    self.object_dict[object_short]=object
                else:
                    new_name = object_short
                    #loops through the objects in the instance that there are multiple duplicate nodes
                    num = 1 
                    while self.window.list_objects.findItems(new_name, QtCore.Qt.MatchExactly):
                        new_name = "%s(%s)" % (object_short, num)
                        num += 1
                    
                    #add item to list and to dictionary
                    self.window.list_objects.addItem (new_name)
                    self.object_dict[new_name] = object
    
    def remove_objects(self):
        #gets all items selected and removes them from the list and the dictionary
        object_files = self.window.list_objects.selectedItems()
        for object in object_files:
            if object.text() in self.object_dict:
                del self.object_dict[object.text()]
            item = self.window.list_objects.takeItem(self.window.list_objects.row(object))
            del item
    
    def add_control(self):
        #takes the first object in a list and uses that object as the control object
        top_objects = mc.ls(sl=1, long=True)
        if top_objects:
            top_object = top_objects[0]

            #sets longname to the variable and display short name (easier for user to read)
            self.control_object = top_object
            self.window.txt_controlObject.setText(top_object.split("|")[-1])
        else:
            #if nothing is selected then it resets the control object to nothing
            self.window.txt_controlObject.setText("")
            self.control_object = ""
    
    def run(self, longname, animated_objects):
        #list all anim curves from objects
        curves = mc.listConnections (animated_objects, type="animCurve")

        #reconnects their input to be driven by the attribute created
        for each_curve in curves:
            mc.connectAttr(self.control_object + "." + longname, each_curve + ".input", force=True)

    def create(self):
        passed_exists = True
        animated_objects = []

        #checks to make sure all fields are filled out, if not prompts
        if self.window.list_objects.count():
            if self.window.txt_attributeName.text():
                if self.window.txt_startTime.text():
                    if self.window.txt_finishTime.text():
                        if self.control_object:
                            if mc.objExists(self.control_object):
                                #checks to make sure each object exist that was specified to have animation
                                for value in self.object_dict.values():
                                    if not mc.objExists(value):
                                        passed_exists = False
                                    else:
                                        #builds list of all objects with animation
                                        if mc.listConnections(value, type="animCurve"):
                                            animated_objects.append(value)
                                if passed_exists:
                                    if animated_objects:
                                        #checks to make sure start time is less than finish time
                                        if int(self.window.txt_startTime.text())< int(self.window.txt_finishTime.text()):
                                            name = self.window.txt_attributeName.text()
                                            #switches nickname to a long name, long names canot have spaces
                                            longname = name.replace("", "_")
                                            if mc.attributeQuery(longname, node=self.control_object, exists=True):
                                                self.dialog("Attribute Exists", "The Attribute that you are trying to create already exists.")
                                            else:
                                                #add attributes and prompts user about completion of script
                                                mc.addAttr(self.control_object, niceName=name, longName=longname, attributeType= "float", keyable=True, hidden=False, maxValue=int(self.window.txt_finishTime.text()), minValue=int(self.window.txt_startTime.text()))
                                                self.run(longname, animated_objects)
                                                self.dialog("Attribute Creation", "Attribute Creation has been completed!")
                                                mc.select(self.control_object)
                                        else:
                                            self.dialog("Timing", "The start time needs to be lesser value than the finish time!")
                                    else:
                                        self.dialog("Animated Objects", "Objects specified have no animation!")
                                else:
                                    self.dialog("Animated Objects", "one or more animation objects no longer exists!")
                            else:
                                self.dialog("Control object", "object doesn't exist: %s" % self.window.txt_controlObject.text())
                        else:
                            self.dialog("Control Object", "No Control object specified")
                    else:
                        self.dialog("Finish Time", "No Finish time specified")
                else:
                    self.dialog("Start Time", "No Start time specified")
            else:
                self.dialog("Attribute Name", "No attribute name specified.")
        else:
            self.dialog("objects added", "There are no objects to get animation from. Please add objects with animation.")



    def dialog(self, title, message):
        #standard confirm dialog to inform user
        mc.confirmDialog(title = title, message = message, button=['ok'])

def attributeAnimationRUn():
    print("launching UI")



def main():
    # 'C:\Users\colton\Documents\maya\scripts\week6\designerInterface\\friendsListInterface.ui'
    parentDir = os.path.split(__file__)[0]

    #parentDir = 'C:\Users\ymz19\Documents\maya\\2020\scripts\WALLE\Animation'
    uiFilePath = os.path.join(parentDir, 'AttributeAnimation.ui')
    
    #interface = UI(uiFilePath)
    aa_window = AttributeAnimationWindow(uiFilePath)
    aa_window._post_ui_setup()


    return aa_window.window

#----copy the following code and run it in your script editor
'''
import WALLE.Animation.AttributeAnimation as anim
import imp
reload(anim) #remove this when shipping
anim_window = anim.main()
anim_window.show()
'''















        