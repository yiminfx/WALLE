import maya.cmds as mc
if mc.window("ram", exists=True):
    mc.deleteUI(ram)

ram = mc.window("Material and Texture", t="Material and Texture", w=300, h=300)
mc.columnLayout(adj=True)
imagePath = mc.internalVar(upd=True) + "icons/scriptlogo.jpg"
mc.image(w=300, h=200, image=imagePath)



# A button to apply any changes
mc.button(label="Apply", command="assign_mat()") # Missing comma after label, and parameter needs to be command.

mc.showWindow(ram)

def assign_mat():
    print ('assigning')