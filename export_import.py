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
    bpy.ops.export_scene.gltf(filepath=target_path, check_existing=True, export_format=format, ui_tab='GENERAL', export_copyright='', export_image_format='AUTO', export_texture_dir='', export_keep_originals=False, export_texcoords=True, export_normals=True, export_draco_mesh_compression_enable=draco, export_draco_mesh_compression_level=6, export_draco_position_quantization=14, export_draco_normal_quantization=10, export_draco_texcoord_quantization=12, export_draco_color_quantization=10, export_draco_generic_quantization=12, export_tangents=False, export_materials=mat, export_original_specular=False, export_colors=True, use_mesh_edges=False, use_mesh_vertices=False, export_cameras=False, use_selection=True, use_visible=False, use_renderable=False, use_active_collection=False, use_active_scene=False, export_extras=False, export_yup=True, export_apply=False, export_animations=skinned, export_frame_range=False, export_frame_step=1, export_force_sampling=False, export_nla_strips=skinned, export_nla_strips_merged_animation_name='Animation', export_def_bones=False, export_anim_single_armature=skinned, export_current_frame=False, export_skins=skinned, export_all_influences=False, export_morph=False, export_morph_normal=False, export_morph_tangent=False, export_lights=False, will_save_settings=False, filter_glob='*.glb;*.gltf')

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
    return obcount


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

    





