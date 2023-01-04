import bpy
import os
from . import functions


def glbExpOp(folderpath,format,ob,draco,material):

    #------------ SPACER ---------------------

    if(material):
        mat = "EXPORT"
    else:
        mat = "NONE"

    #------------ SPACER ---------------------

    functions.forceSelectable(ob)
    file_name = ob.name
    print(file_name)
    target_path =os.path.join(folderpath, file_name)
    functions.forceselect(ob)
    bpy.ops.export_scene.gltf(filepath=target_path, check_existing=True, export_format=format, ui_tab='GENERAL', export_copyright='', export_image_format='AUTO', export_texture_dir='', export_keep_originals=False, export_texcoords=True, export_normals=True, export_draco_mesh_compression_enable=draco, export_draco_mesh_compression_level=6, export_draco_position_quantization=14, export_draco_normal_quantization=10, export_draco_texcoord_quantization=12, export_draco_color_quantization=10, export_draco_generic_quantization=12, export_tangents=False, export_materials=mat, export_original_specular=False, export_colors=True, use_mesh_edges=False, use_mesh_vertices=False, export_cameras=False, use_selection=True, use_visible=False, use_renderable=False, use_active_collection=False, use_active_scene=False, export_extras=False, export_yup=True, export_apply=False, export_animations=False, export_frame_range=False, export_frame_step=1, export_force_sampling=False, export_nla_strips=False, export_nla_strips_merged_animation_name='Animation', export_def_bones=False, export_anim_single_armature=False, export_current_frame=False, export_skins=False, export_all_influences=False, export_morph=False, export_morph_normal=False, export_morph_tangent=False, export_lights=False, will_save_settings=False, filter_glob='*.glb;*.gltf')


def glbExp(draco,material):
    format = 'GLB'
    mainfolderpath = bpy.context.scene.saveFolderPath
    folderpath =os.path.join(mainfolderpath, "models")

    #------------ SPACER ---------------------

    colName = "Scene Objects"
    coll = functions.findCollection(colName)
    for ob in coll.objects:
        glbExpOp(folderpath,format,ob,draco,material)

    colName = "Scene Instances"
    collmain = functions.findCollection(colName)
    for coll in collmain.children:
        count = 0
        for ob in coll.objects:
            if(count == 0):
                glbExpOp(folderpath,format,ob,draco,material)
            count += 1
        

    return