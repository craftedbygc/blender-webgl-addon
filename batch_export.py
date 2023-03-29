import bpy
import os
from . import functions



def restUpdateState():
    nameArray = ["Objects","Rigged Objects","Instances Manual","Instances Nodes"]
    allColls = functions.getDifNamesColl(nameArray)
    for coll in allColls:
        if(coll.name == nameArray[0]):
            for ob in coll.objects:
                if(ob.type == 'MESH'):
                    functions.createProp(ob,"updated",1)
        if(coll.name == nameArray[1]):
            for ob in coll.objects:
                if(ob.type == 'MESH'):
                    functions.createProp(ob,"updated",1)
        if(coll.name == nameArray[2]):
            for cc in coll.children:
                count = 0
                for ob in cc.objects:
                    if(count == 0):
                        functions.createProp(ob,"updated",1)
        if(coll.name == nameArray[3]):
            for cc in coll.children:
                if("Instanced Geometry" in cc.name):     
                    for ob in cc.objects:
                        functions.createProp(ob,"updated",1)
                    for ccc in cc.children:
                        for ob in ccc.objects:
                            functions.createProp(ob,"updated",1)
         
            

def glbExpOp(folderpath,format,coll,ob,draco,material,skinned,keepOrigin=False):

    #------------ SPACER ---------------------
    if(material):
        mat = "EXPORT"
    else:
        mat = "NONE"

    #------------ SPACER ---------------------

    functions.forceSelectable(ob)

    is_empty = ob.type == 'EMPTY'
    if(is_empty):
        return
        
    file_name = ob.name
    file_name = functions.namingConvention(file_name)
    target_path =os.path.join(folderpath, file_name)

    #------------ SPACER ---------------------
    prevLoc, prevRot, prevSac = functions.geoCleaner(ob,skinned,keepOrigin)

    #------------ SPACER ---------------------
    functions.forceselect(ob)
    bpy.ops.export_scene.gltf(filepath=target_path, check_existing=True, export_format=format, ui_tab='GENERAL', export_copyright='', export_image_format='AUTO', export_texture_dir='', export_keep_originals=False, export_texcoords=True, export_normals=True, export_draco_mesh_compression_enable=draco, export_draco_mesh_compression_level=6, export_draco_position_quantization=14, export_draco_normal_quantization=10, export_draco_texcoord_quantization=12, export_draco_color_quantization=10, export_draco_generic_quantization=12, export_tangents=False, export_materials=mat, export_original_specular=False, export_colors=True, use_mesh_edges=False, use_mesh_vertices=False, export_cameras=False, use_selection=True, use_visible=False, use_renderable=False, use_active_collection=False, use_active_scene=False, export_extras=False, export_yup=True, export_apply=False, export_animations=skinned, export_frame_range=False, export_frame_step=1, export_force_sampling=False, export_nla_strips=skinned, export_nla_strips_merged_animation_name='Animation', export_def_bones=False, export_anim_single_armature=skinned, export_current_frame=False, export_skins=skinned, export_all_influences=False, export_morph=False, export_morph_normal=False, export_morph_tangent=False, export_lights=False, will_save_settings=False, filter_glob='*.glb;*.gltf')
    print("OBJECT EXPORTED >>> ",ob.name)

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


def checkAndExport(folderpath,format,coll,ob,draco,material,obcount,skinned,keepOrigin=False):
    autoCheck = bpy.context.scene.checkUpdates == True
    if obcount is None:
        obcount = 0

    if(autoCheck):
        bpy.context.view_layer.update()
        prop = functions.getproperty(ob,"updated")
        if(prop > 0):
            glbExpOp(folderpath,format,coll,ob,draco,material,skinned,keepOrigin)
            ob["updated"] = 0
            obcount += 1
            return obcount
        else:   
            if(prop == False):
                functions.createProp(ob,"updated",0)
            return obcount  
    else:
        glbExpOp(folderpath,format,coll,ob,draco,material,skinned,keepOrigin)
        functions.createProp(ob,"updated",0)
        obcount += 1
        return obcount


def glbExp(draco,material):
    format = 'GLB'
    mainfolderpath = bpy.context.scene.saveFolderPath
    folderpath =os.path.join(mainfolderpath, "models")


    print("========================= #") 
    print("========================= #")
    print("BATCH START") 
    print("========================= #")
    print("========================= #") 


    #------------ SPACER ---------------------
    
    obcount = 0

    colName = "Objects"
    coll = functions.findCollection(colName)
    for ob in coll.objects:
        if ob is not None and ob.type == 'MESH': 
            obcount = checkAndExport(folderpath,format,coll,ob,draco,material,obcount,skinned=False,keepOrigin=False)

    #------------ SPACER ---------------------
    
    colName = "Rigged Objects"
    coll = functions.findCollection(colName)
    for ob in coll.objects:   
        if ob is not None and ob.type == 'MESH':
            obcount = checkAndExport(folderpath,format,coll,ob,draco,material,obcount,skinned=True,keepOrigin=False)
                
    #------------ SPACER ---------------------

    colName = "Instances Manual"
    coll = functions.findCollection(colName)
    if coll is not None:
        for cc in coll.children:
            count = 0
            for ob in cc.objects:
                if ob is not None and ob.type == 'MESH':
                    if(count == 0):
                        obcount = checkAndExport(folderpath,format,coll,ob,draco,material,obcount,skinned=False,keepOrigin=False)     
                    count += 1
    
    #------------ SPACER ---------------------

    colName = "Instances Nodes"    
    coll = functions.findCollection(colName)
    if coll is not None:
        for cc in coll.children: 
            if("Instanced Geometry" in cc.name):     
                for ob in cc.objects:
                    if ob is not None and ob.type == 'MESH':
                        obcount = checkAndExport(folderpath,format,coll,ob,draco,material,obcount,skinned=False,keepOrigin=True)
                for ccc in cc.children:
                    for ob in ccc.objects:
                        if ob is not None and ob.type == 'MESH':
                            obcount = checkAndExport(folderpath,format,coll,ob,draco,material,obcount,skinned=False,keepOrigin=True) 
        

    finalCount = obcount
    
    print("========================= #") 
    print("========================= #")
    print("BATCH EXPORT DONE") 
    print("- Total Objects Exported:",finalCount)
    print("========================= #")
    print("========================= #") 

