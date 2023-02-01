import bpy
import os
from bpy.props import *
import time
import json
import math

class DataExport(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Data Exporter"
    bl_idname = "OBJECT_PT_GCDataExport"
    bl_category = "InstanceExport"
    
    def draw(self, context):
        layout = self.layout
        sce = context.scene
        row = layout.row()
        row.label(text="Object Data Export Options", icon ="SCENE_DATA")
        layout.prop(sce,'data_path')
        layout.prop(sce,'my_global_data_name')
        layout.prop(sce,"my_global_pos")
        layout.prop(sce,"my_global_rot")
        layout.prop(sce,"my_global_sac")
        layout.prop(sce,"my_global_cus")
        layout.prop(sce,"my_global_minify")
        layout.prop(sce, "my_global_base")
        row = layout.row()
        row = layout.row()
        row = layout.row()
        row = layout.row()
        row = layout.row()
        row = layout.row()
        row = layout.row()
        props = row.operator("scene.dataexport", icon ="EXPORT")
        props.data_name = sce.my_global_data_name
        props.export_data_string = sce.data_path
        props.minify_state = sce.my_global_minify
        props.pos_state = sce.my_global_pos
        props.rot_state = sce.my_global_rot
        props.sac_state = sce.my_global_sac
        props.cus_state = sce.my_global_cus
        props.base_state = sce.my_global_base
        


class DataInstanceExport(bpy.types.Operator):
    """Script to export for wegbl"""
    bl_idname = "scene.dataexport"
    bl_label = "Export Data"
    
    #create properties
    
    data_name :  bpy.props.StringProperty(
        name="File Name",
        default = "objectdata",
    )
    
    export_data_string :  bpy.props.StringProperty(
        name="Export Data Path",
    )
    
    export_data_string :  bpy.props.StringProperty(
        name="Export Data Path",
    )
    
    minify_state :  bpy.props.BoolProperty(
        name="Minify",
        default = True,
    )
    pos_state :  bpy.props.BoolProperty(
        name="Position",
        default = True,
    )
    rot_state :  bpy.props.BoolProperty(
        name="Rotation",
        default = True,
    )
    sac_state :  bpy.props.BoolProperty(
        name="Scale",
        default = True,
    )
    cus_state :  bpy.props.BoolProperty(
        name="Custom Props",
        default = False,
    )
    base_state :  bpy.props.BoolProperty(
        name="Separate instances by base",
        default = False,
    )
    
    def execute(self, context):
        # Save file and get file path
        print("SCRIPT START - SAVING BLEND FILE ")
        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)

        dataFolder_path = self.export_data_string
        
        def rd(e):
            return round(e, 4)
        
        def createInstance(objects,collName,instance,objectName):
            name = objectName
            data = []
            
            # Get the world matrix
            mat = instance.matrix_world
            # extract components back out of the matrix as two vectors and a quaternion
            pos, rot, sca = mat.decompose()
            
            pos = [rd(pos.x),rd(pos.z),rd(-pos.y)]
            data.append(pos)
            
            rot = [rd(rot[1]), rd(rot[2]), rd(rot[3]), rd(rot[0])]
            data.append(rot)
            
            sca = [rd(sca.x),rd(sca.y),rd(sca.z)]  
            data.append(sca)
            
            # Get the UVs - optional
            uv = instance.uv
            
            objects[collName].append(data)
        
        def exportUnseenFormat():
            # Set File Path ============================================================== #
            file = self.data_name + ".unseen"
            filepath = os.path.join(dataFolder_path, file)

            # Set Main Object ============================================================== #
            objects = {}

                 # Open/Create Unseen file ============================================================== #
            f = open(filepath, "w")
            bpy.context.scene.frame_set(0)

            # Get evaluated dependency graph of the scene ============================================================== #
            depsgraph = bpy.context.evaluated_depsgraph_get()

       
            
            # Write Info Into Unseen File ============================================================== #
            for coll in bpy.data.collections:
                if("-geo-instances" in coll.name):
                    
                    sname = coll.name[:-14] # Get name of collection 
                    count = 0
                    # Get the names of all objects in that collection
                    myList = [obj.name for obj in coll.all_objects]
                    myList = sorted(myList)
                    
                    if(self.base_state):
                        print('Separating instances based on the base object')
                        objects[sname] = [] # Save per base object
                    
                    for name in myList:
                        # Get the base object on which there's instances
                        ob = coll.all_objects[name]
                        # Get the object in the evaluated dependency graph to attach instances
                        evalOb = ob.evaluated_get(depsgraph)
                        
                        # Go through all the instances in the scene
                        for object_instance in depsgraph.object_instances:
                            # Get only the instances that are instanced on the object in the collection.
                            if object_instance.parent == evalOb:
                                
                                # This is the original object that is instanced.
                                obj = object_instance.object
                                instance_name = obj.name
                                
                                if not (self.base_state):
                                    # Save per instance object
                                    if instance_name not in objects:
                                        objects[instance_name] = [] # Save per type of object that's instanced
                                
                                # `is_instance` denotes whether the object is coming from instances (as an opposite of
                                # being an emitting object. )
                                if object_instance.is_instance: # Check that it is an instance
                                    print(f"Instance of {instance_name}")
                                    obName = count
                                    if (selaf.base_state):
                                        print('Separating instances based on the base object')
                                        createInstance(objects, sname, object_instance, obName) # Save per base object
                                    else:
                                        createInstance(objects, instance_name, object_instance, obName) # Save per instance object                
                                    count += 1
            
            if(self.minify_state):
                indentVal = None
            else:
                indentVal = 1
                
            objects = json.dumps(objects, indent=indentVal, ensure_ascii=True,separators=(',', ':'))
            print(objects)
            f.write(objects)
            f.close()
            
            return
        
        ## Run Functions --------------- ##     

        exportUnseenFormat()
            
        return {"FINISHED"}


def register():
    bpy.utils.register_class(DataInstanceExport)
    bpy.utils.register_class(DataExport)
    
    bpy.types.Scene.data_path = bpy.props.StringProperty(
      name = "Path",
      default = "",
      description = "Define the root path of the project",
      subtype = 'DIR_PATH'
    )
    
    bpy.types.Scene.my_global_data_name = bpy.props.StringProperty(
      name = "Name",
      default = "objectdata",
      description = "Define name for the data object",
      subtype = 'FILE_NAME'
    )
    
    bpy.types.Scene.my_global_prs = bpy.props.BoolProperty(
        name="Export ObjectData",
        description="Export Postions Rotation Scale of Files",
        default = False,
    )
    
    bpy.types.Scene.my_global_minify = bpy.props.BoolProperty(
        name="Minify",
        description="Remove indentation for export",
        default = True,
    )
    
    bpy.types.Scene.my_global_pos = bpy.props.BoolProperty(
        name="Position",
        description="Export Position",
        default = True,
    )
    
    bpy.types.Scene.my_global_rot = bpy.props.BoolProperty(
        name="Rotation",
        description="Export Rotation",
        default = True,
    )
    
    bpy.types.Scene.my_global_sac = bpy.props.BoolProperty(
        name="Scale",
        description="Export Scale",
        default = True,
    )
    
    bpy.types.Scene.my_global_cus = bpy.props.BoolProperty(
        name="Custom Properties",
        description="Export Custom Props",
        default = False,
    )
    
    bpy.types.Scene.my_global_base = bpy.props.BoolProperty(
        name="Separate instances by base",
        description="Export Instances separated based on the object on which they're instanced (as opposed to the original geometry). Name key based on collection name. NOTE: Not particularly useful with different object instances on one base object.",
        default = False,
    )


def unregister():
    bpy.utils.unregister_class(DataInstanceExport)
    bpy.utils.unregister_class(DataExport)


if __name__ == "__main__":
    register()
