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
    file_name = functions.tagsRemoval(file_name)
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


#------------ SPACER ---------------------
#------------ SPACER ---------------------
#------------ SPACER --------------------- 
def update_mesh():
    meshsfolder = bpy.context.scene.updateMeshFolder
    selected_objects = bpy.context.selected_objects
    for obj in selected_objects:
        if obj.type == 'MESH':
            formats = (".abc",".obj",".fbx")
            for format in formats:
                file = os.path.join(meshsfolder, obj.name + format)
                if os.path.isfile(file):
                    if len(obj.material_slots) > 0:
                        obj_material = obj.data.materials[0]
                    if("abc" in format):
                        bpy.ops.wm.alembic_import(filepath=file)
                    if("obj" in format):
                        bpy.ops.import_scene.obj(filepath=file)
                    if("fbx" in format):
                        bpy.ops.import_scene.fbx(filepath=file)
                    imported_obj = bpy.context.active_object
                    obj.data = imported_obj.data
                    if len(obj.material_slots) > 0:
                        obj.data.materials.clear()
                        obj.data.materials.append(obj_material)
                    bpy.ops.object.select_all(action='DESELECT')
                    imported_obj.select_set(True)
                    bpy.ops.object.delete()


#------------ SPACER ---------------------
#------------ SPACER ---------------------
#------------ SPACER --------------------- 
def update_create_material():
    textureFolder = bpy.context.scene.textureFolder
    selected_objects = bpy.context.selected_objects
    for obj in selected_objects:
        print("CREATE MATERIAL FOR:",obj.name)
        if obj.type == 'MESH':
            formats = (".png",".jpeg",".tiff")
            material = bpy.data.materials.new(name="PrincipledMaterial")
            material.use_nodes = True
            node_tree = material.node_tree
            principled_node = node_tree.nodes.get('Principled BSDF')
            principled_node.location = (0, 0)
            material.name = obj.name + "-active-mat"
            output_node = node_tree.nodes['Material Output']
            output_node.location = (300, 0)
            for format in formats:
                maps = ("-color","-roughness","-normal")
                for map in maps:
                    file = os.path.join(textureFolder, obj.name + map + format)
                    print("Creating:",file)
                    if os.path.isfile(file):
                        image_texture_node = node_tree.nodes.new('ShaderNodeTexImage')
                        image_texture_node.image = bpy.data.images.load(file)
                        if "color" in map:
                            node_tree.links.new(image_texture_node.outputs['Color'], principled_node.inputs['Base Color'])
                            image_texture_node.location = (-300, 0)
                        if "roughness" in map:
                            node_tree.links.new(image_texture_node.outputs['Color'], principled_node.inputs['Roughness'])
                            image_texture_node.image.colorspace_settings.name = 'Raw'
                            image_texture_node.location = (-300, -300)
                        if "normal" in map:
                            node_tree.links.new(image_texture_node.outputs['Color'], principled_node.inputs['Normal'])
                            image_texture_node.image.colorspace_settings.name = 'Raw'
                            image_texture_node.location = (-300, -600)

            if obj.data.materials:
                obj.data.materials[0] = material
            else:
                obj.data.materials.append(material)
