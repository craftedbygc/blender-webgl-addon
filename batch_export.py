import bpy
import os
from . import functions

def restUpdateState():
    allColls = functions.getDifNamesColl(["Objects","Instances Manual"])
    for coll in allColls:
        for ob in coll.objects:
            functions.createProp(ob,"updated",1)
    


def glbExpOp(folderpath,format,coll,ob,draco,material):

    #------------ SPACER ---------------------

    if(material):
        mat = "EXPORT"
    else:
        mat = "NONE"

    #------------ SPACER ---------------------

    functions.forceSelectable(ob)
    file_name = ob.name
    #file_name = functions.nameMatchScene(file_name,coll.name)
    file_name = functions.namingConvention(file_name)
    target_path =os.path.join(folderpath, file_name)

    #------------ SPACER ---------------------
    # TBA-NEEDS-REVISION
    functions.geoCleaner(ob)

    #------------ SPACER ---------------------
    functions.forceselect(ob)
    bpy.ops.export_scene.gltf(filepath=target_path, check_existing=True, export_format=format, ui_tab='GENERAL', export_copyright='', export_image_format='AUTO', export_texture_dir='', export_keep_originals=False, export_texcoords=True, export_normals=True, export_draco_mesh_compression_enable=draco, export_draco_mesh_compression_level=6, export_draco_position_quantization=14, export_draco_normal_quantization=10, export_draco_texcoord_quantization=12, export_draco_color_quantization=10, export_draco_generic_quantization=12, export_tangents=False, export_materials=mat, export_original_specular=False, export_colors=True, use_mesh_edges=False, use_mesh_vertices=False, export_cameras=False, use_selection=True, use_visible=False, use_renderable=False, use_active_collection=False, use_active_scene=False, export_extras=False, export_yup=True, export_apply=False, export_animations=False, export_frame_range=False, export_frame_step=1, export_force_sampling=False, export_nla_strips=False, export_nla_strips_merged_animation_name='Animation', export_def_bones=False, export_anim_single_armature=False, export_current_frame=False, export_skins=False, export_all_influences=False, export_morph=False, export_morph_normal=False, export_morph_tangent=False, export_lights=False, will_save_settings=False, filter_glob='*.glb;*.gltf')


def glbExp(draco,material,autoCheck):
    format = 'GLB'
    mainfolderpath = bpy.context.scene.saveFolderPath
    folderpath =os.path.join(mainfolderpath, "models")


    print("========================= #") 
    print("========================= #")
    print("BATCH START") 
    print("========================= #")
    print("========================= #") 


    #------------ SPACER ---------------------

    colName = "Objects"
    coll = functions.findCollection(colName)
    obcount = 0
    for ob in coll.objects:
        if(autoCheck):
            bpy.context.view_layer.update()
            prop = functions.getproperty(ob,"updated")
            if(prop > 0):
                    glbExpOp(folderpath,format,coll,ob,draco,material)
                    ob["updated"] = 0
                    obcount += 1
            else:
                print("BATCH START") 
                if(prop == False):
                    functions.createProp(ob,"updated",0)
        else:
             glbExpOp(folderpath,format,coll,ob,draco,material)
             functions.createProp(ob,"updated",0)
             obcount += 1

                
                
    #------------ SPACER ---------------------

    colName = "Instances Manual"
    coll = functions.findCollection(colName)
    instcount = 0
    for cc in coll.children:
        count = 0
        for ob in cc.objects:
            if(autoCheck):
                bpy.context.view_layer.update()
                prop = functions.getproperty(ob,"updated")
                if(prop > 0):
                        glbExpOp(folderpath,format,coll,ob,draco,material)
                        ob["updated"] = 0
                        instcount += 1
                else:
                    if(prop == False):
                        functions.createProp(ob,"updated",0)
            else:
                glbExpOp(folderpath,format,coll,ob,draco,material)
                functions.createProp(ob,"updated",0)
                instcount += 1         
            count += 1
    
    #------------ SPACER ---------------------

    colName = "Instances Nodes"    
    coll = functions.findCollection(colName)
    nodecount = 0
    for cc in coll.children: 
        if("Instanced-Geometry" in cc.name):     
            for ob in cc.objects:
                if(autoCheck):
                    bpy.context.view_layer.update()
                    prop = functions.getproperty(ob,"updated")
                    if(prop > 0):
                        glbExpOp(folderpath,format,coll,ob,draco,material)
                        ob["updated"] = 0
                        nodecount += 1
                    else:
                        if(prop == False):
                            functions.createProp(ob,"updated",0)
                else:
                    glbExpOp(folderpath,format,coll,ob,draco,material)
                    functions.createProp(ob,"updated",0)
                    nodecount += 1
           
 

    finalCount = instcount + obcount + nodecount
    
    print("========================= #") 
    print("========================= #")
    print("BATCH EXPORT DONE") 
    print("- Total Objects Exported:",finalCount)
    print("========================= #")
    print("========================= #") 

