import maya.cmds as mc
if mc.window("ram", exists=True):
    mc.deleteUI(ram)

ram = mc.window("Material and Texture", t="Material and Texture", w=300, h=300)
mc.columnLayout(adj=True)
imagePath = mc.internalVar(upd=True) + "icons/scriptlogo.jpg"
mc.image(w=300, h=200, image=imagePath)

# A dropdown menu deisnged to change material/color of octopus
matOptionMenu = mc.optionMenu(label="Material") # Need to assign a variable here to capture its full name.
myBlinn = mc.menuItem(label="Red")
myBlinn = mc.menuItem(label="Blue")
myBlinn = mc.menuItem(label="Yellow")
myBlinn = mc.menuItem(label="Green")
myBlinn = mc.menuItem(label="Orange")
myBlinn = mc.menuItem(label="Purple")

# A slider designed to alter the intensity of the octopus' texture
mc.intSliderGrp(label="Texture", min=0, max=10, field=True)

# A button to apply any changes
mc.button(label="Apply", command="applyMaterial()") # Missing comma after label, and parameter needs to be command.

mc.showWindow(ram)

def applyMaterial():
   currentValue = mc.optionMenu(matOptionMenu, query=True, value=True) # Use the variable to get the value.
   if currentValue == "Red":
       mc.hyperShade(objects='lambert1')
       mc.hyperShade(assign='red')
   elif currentValue == "Blue":
       mc.hyperShade(objects='lambert1')
       mc.hyperShade(assign='blue')
   elif currentValue == "Yellow":
       mc.hyperShade(objects='lambert1')
       mc.hyperShade(assign='yellow')
   elif currentValue == "Green":
       mc.hyperShade(objects='lambert1')
       mc.hyperShade(assign='green')
   elif currentValue == "Orange":
       mc.hyperShade(objects='lambert1')
       mc.hyperShade(assign='orange')
   elif currentValue == "Purple":
       mc.hyperShade(objects='lambert1')
       mc.hyperShade(assign='purple')