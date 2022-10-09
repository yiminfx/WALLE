import maya.cmds as mc
import os



def increment_shot_file():

    filepath = mc.file(q=True, sn=True)
    filename = os.path.basename(filepath)

    find_index = filepath.rfind('_v')
    if (find_index):
        file_string = filepath[:find_index+2]
        version_num_string = filepath[find_index+2:]

        version_num=version_num_string.split('.')[0]
        extension =version_num_string.split('.')[1]

        next_version_num = int(version_num)+1

        #figure out the padding
        string_len = len(version_num)

        next_version_string = str(next_version_num).rjust(string_len, '0')
        new_maya_path = file_string + next_version_string+'.'+extension

        print(new_maya_path)
        mc.file(rename=new_maya_path)
        mc.file(save=True)
    else:
        print('unable to version up. please find if the file is formatted properly')


