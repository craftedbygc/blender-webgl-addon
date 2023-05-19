import bpy
import os
import addon_utils
from . import functions

addon_utils.enable("io_scene_fbx")

#------------ SPACER ---------------------
#------------ SPACER ---------------------
#------------ SPACER ---------------------           

def glbExpOp(folderpath,format,ob,draco,obcount,skinned):

    modelFolder =os.path.join(folderpath, "models")

    #------------ SPACER ---------------------
    # if(material):
    #     mat = "EXPORT"
    # else:
    #     mat = "NONE"
    mat = "NONE"
    #------------ SPACER ---------------------

    functions.forceSelectable(ob)

    is_empty = ob.type == 'EMPTY'
    if(is_empty):
        return
        
    file_name = ob.name
    file_name = functions.namingConvention(file_name)
    target_path =os.path.join(modelFolder, file_name)

    #------------ SPACER ---------------------
    prevLoc, prevRot, prevSac = functions.geoCleaner(ob,skinned)

    #------------ SPACER ---------------------
    functions.forceselect(ob)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = None
    ob.select_set(True)
    
    if(skinned):
        parent = ob.parent
        parent.select_set(True)

    bpy.context.view_layer.objects.active = bpy.data.objects[ob.name]

    print("TBA-6",skinned)
    bpy.ops.export_scene.gltf(filepath=target_path,export_format=format, export_texcoords=True, export_normals=True, export_draco_mesh_compression_enable=draco, export_materials=mat,export_colors=True, export_attributes=True, use_selection=True, export_yup=True, export_animations=skinned, export_frame_range=skinned,export_skins=skinned)
    
    file_name = file_name+".glb"
    load_path =os.path.join(modelFolder, file_name)
    file_size = os.path.getsize(load_path)
    file_size_mb = file_size / (1024 * 1024)

    print("HERE",file_size_mb)
    #------------ SPACER ---------------------
    if(skinned):
        parent = ob.parent
        parent.location = prevLoc
        parent.rotation_euler = prevRot
        parent.scale = prevSac
    else:
        ob.location = prevLoc
        ob.rotation_euler = prevRot
        ob.scale = prevSac
        
    obcount += 1
    return obcount, file_size_mb


#------------ SPACER ---------------------
#------------ SPACER ---------------------
#------------ SPACER --------------------- 

def c4d_import():
    fbx_file_path = "path_to_your_fbx_file"
    bpy.ops.import_scene.fbx(filepath=fbx_file_path)

    obcoll = functions.findCollection("Objects")
    imported_object = [ob for ob in bpy.context.selected_objects]

    for ob in imported_object:
        functions.forceselect(ob)
        ob.scale *=0.01
        obcoll.objects.link(ob)

def c4d_export():
    fbx_file_path = "path_to_your_fbx_file"
    bpy.ops.import_scene.fbx(filepath=fbx_file_path)

    obcoll = functions.findCollection("Objects")
    prevScale = 1
    if obcoll is not None:
        for ob in obcoll.objects:
            functions.forceselect(ob)
            prevScale = ob.scale
            ob.scale *= 100
    else:
        print("No Objects Collections To export")

    





