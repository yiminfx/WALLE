

import os
import shutil
import stat
import maya.OpenMaya as om
import maya.cmds as mc
import maya.app.general.fileTexturePathResolver as ftpr

import datetime as dt

class FileDependencies(object):
    '''
    object that represents the scene and its dependencies, texture files, cache etc
    '''
    logger= None
    def __init__(self, logger=None):
        self.file_textures = {}
        self._shared_textures = []

        current_time = dt.date.today()
        self.year = int(current_time.year)
        self.month = int(current_time.month)
        self.day = int(current_time.day)
        self.logger=logger



    def write_logger(self, message):
        '''
        writes to logger if it exists. if not just prints
        arg:
            message(str): the message to log or print
        '''
        #TODO: fix this 
        if self.logger!=None:
            self.logger.info(message)
        else:
            print(message)
        
        #print(message)
    def image_attr(self, node):
        #gets the texture or plane name
        attribute_name = 'fileTextureName'
        if mc.objectType(node)!= 'file':
            attribute_name='imageName'
        image_attribute='%s.%s' % (node,attribute_name)
        return image_attribute

    def get_file_textures(self):
        '''
        used to get all the textures in the scene and store them
        '''
        #gets all file node textures
        all_file_nodes = mc.ls(type=['file', 'imagePlane'], long=True)
        for each_file_node in all_file_nodes:
            self.write_logger('found nodes to copy %s'% each_file_node)
            #check if its a sequence
            sequence=mc.getAttr('%s.useFrameExtension' % each_file_node)

            #gets the texture or image plane name
            link = mc.getAttr(self.image_attr(each_file_node))

            all_files = []
            # if its a sequence gets all the images in the sequence
            if sequence:
                file_node_data = self.get_image_sequence(link)
                all_files+= file_node_data[0]
            else:
                # if its not a sequence just adds the file
                all_files +=[link]
            #add all files to the file node of depency type file
            self.file_textures[each_file_node] = all_files

            #checks for a shared tag
            if mc.attributeQuery('tex_shared', node=each_file_node, exists=1):
                if mc.getAttr('%s.%s' % (each_file_node, 'tex_shared')):
                    self._shared_textures.append(each_file_node)
        print('')
        print(self._shared_textures)
        print('\n')






    
    def get_image_sequence (path, is_sequence=True, uv_mode=0):
        '''
        given a file path, determine if it contains <f> or <UDIM> to get all the files in the sequence

        args:
            path(str): file path
            is_sequence(bool):wether the file should be treated as a image sequence
            uv_mode()
        '''
        all_files = []
        sequence_path = ftpr.getFilePatternString(path, is_sequence,uv_mode)

        #maya is case sensitive with udim
        if any(x for x in ['<f>', '<UDIM>'] if x.lower() in sequence_path.lower()):
            all_files = ftpr.findAllFilesForPattern(sequence_path, None)
        return [all_files, sequence_path]


    def move_textures(self, source_template=None, destination_template=None, 
                    unknown_template=None, extra_fields=None, set_unkowns_True=True, all_lower=False, shared_dest_template=None, custom_path=None):
        '''
        used to move textures from current path to a path specified by template and output directory.
        args:
            source_template(templated path): the template to use to extract fields from the source path
            destination_template(templatePath):the template to use to create the destination path
            unknown_template(templatePath): the template to use to create the destination if the source file does not adhere to the source template
            extra_fields(dict[str, Any]): a dictionary of supplemental fields for use in templates
            set_unkowns (bool): unused
            all_lower(bool): force the destination path to lower case before writing files
            shared_dest_template (templatePath): an alternate destination template
            custom_path(str): if provided, will replace the root path of the template, it the show folder
        '''
        self.write_logger('\n---moving dependencies: texture files----')
        moved_textures = []
        #set basic fields if theres file texture nodes
        if not self.file_textures:
            return
        
        shader_types = mc.listNodeTypes('shader')
        for each_node in self.file_textures:
            self.write_logger('Node to copy: %s' % each_node)
            if self.file_textures[each_node]:
                for each_file in self.file_textures[each_node]:
                     self.write_logger('file path: %s' % each_file)
                     fields = {}
                     #set basic fields

                     fields['YYYY'] = self.year
                     fields['MM'] = self.month
                     fields['DD'] = self.day

                     this_dest_template = destination_template
                     if (shared_dest_template is not None 
                                and each_node in self._shared_textures):
                                this_dest_template=shared_dest_template
                    
                     if (os.path.isfile(each_file)):
                            #shader_types = mc.listNodeTypes('shader')
                            materials = self.materials_from_file(each_node, shader_types=shader_types)
                     

                            
                            if materials:
                                material = materials[0]
                            else:
                                material='None'
                            fields['materialname']=material
                            try:
                                #tries to update the fields with fields from the file path
                                fields.update(source_template.get_fields(os.path.realpath(each_file)))
                                if 'variation' not in fields:
                                    fields['variation'] = 'unkown'
                            except Exception as e:
                                #back up template if we couldnt get fields from source template
                                self.write_logger('using unknown template: ' + str(e))
                                this_dest_template=unknown_template
                                #get file name of the file
                                fields['filename'] = os.path.basename(each_file)
                            #use fields and template to get destination for the path
                            destination_path = custom_path +'/' +os.path.basename(each_file)

                            if extra_fields:
                                fields.update(extra_fields)

                            if each_file not in moved_textures:
                                
                                if not os.path.exists(destination_path):
                                    #use copy2
                                    shutil.copy2(each_file, destination_path)
                                    #sets it to be writable
                                os.chmod(destination_path, stat.S_IWRITE)

                                    #log or prints the notification
                                self.write_logger('copied texture: %s to %s' % (each_file,destination_path))
                                mc.setAttr(self.image_attr(each_node), destination_path, type='string')
                                moved_textures.append(each_file)
                            else:
                                #logs or prints notifications
                                self.write_logger('texture already copied: %s' % destination_path)
                                mc.setAttr(self.image_attr(each_node), destination_path, type='string')
                     else:
                        self.write_logger('texture doesnt exist %s' % each_file)

                        

                                

    def materials_from_file(self, file_node, shader_types=None):
        '''
        get a list of materials connected to a file node

        args:
            file_node(str):name of the file node
            shader_type(list[str]): list of shader types

        returns:
            materials (list[str]): names of materials connectd
        '''
        if not shader_types:
            shader_types = mc.listNodeTypes('shader')
        shader_types = set(shader_types)

        materials=[]

        #create a mselectionList with our selected items
        sel_list= om.MSelectionList()
        sel_list.add(file_node)
        mobject = om.MObject() # the current object
        sel_list.getDependNode(0, mobject)

        #create a dependency graph iterator for our current object:
        mit_dependency_graph = om.MItDependencyGraph(mobject,om.MItDependencyGraph.kUpstream)
        while not mit_dependency_graph.isDone():
            current_item=mit_dependency_graph.currentItem()
            dependency_node =om.MFnDependencyNode(current_item)
            if dependency_node.typeName() in shader_types:
                name = dependency_node.name()
                materials.append(name)
            mit_dependency_graph.next()

        return materials