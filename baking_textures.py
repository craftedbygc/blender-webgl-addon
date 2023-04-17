import bpy
import os
from . import functions


def bake_maps():
    mainfolderpath = bpy.context.scene.saveFolderPath
    folder_path = os.path.join(mainfolderpath, "textures")
    bpy.context.scene.exportState = True

    #Set the viewport to MATERIAL preview so it does not impact the render
    bpy.context.space_data.shading.type = 'MATERIAL'
    bpy.context.scene.render.engine = "CYCLES"


    # Set the render device to GPU
    bpy.context.scene.cycles.device = 'GPU'

    #Get the active object to render the lightmap
    ob = bpy.context.active_object


    #Create a new image and name it accordingly to the convention
    new_name = ob.name  +"-"+ "light-map" 
    covName = functions.namingConvention(new_name)
    file_name = covName + ".png"
    bake_file_path = os.path.join(folder_path,file_name)
 
    #Create the in iamge to bake into
    tex_size = 2048
    baked_image = bpy.data.images.new(covName,width=tex_size,height=tex_size)
    print("TBA-LEVEL-1")
    if len(ob.material_slots)>0:
        mat = ob.material_slots[0].material
        if mat is not None and mat.use_nodes:
            node_tree= mat.node_tree
            nodes = node_tree.nodes

            #Create the node for the image and add the previous create baking image
            image_texture_node = nodes.new(type="ShaderNodeTexImage")
            image_texture_node.image = baked_image

            # Set bake Settings - needs to come from the UI
            bk_type = "COMBINED"
            bpy.context.scene.cycles.bake_type = bk_type
            bpy.context.scene.cycles.samples = 128 
            bpy.context.scene.render.bake.use_pass_direct = True
            bpy.context.scene.render.bake.use_pass_indirect = True
            bpy.context.scene.render.bake.use_pass_color = True

            #Bake Lighting
            print("TBA-LEVEL-2")
            bpy.ops.object.bake(type=bk_type)

            #Save image
            baked_image.filepath_raw = bake_file_path
            baked_image.file_format = 'PNG'
            baked_image.save()

            # Connect baked Image to the principle shader socket 
            bsdf_principled_node = None
            for node in nodes:
                if node.type == 'BSDF_PRINCIPLED':
                    bsdf_principled_node = node
                    break

            if bsdf_principled_node is not None:
                base_color_input = bsdf_principled_node.inputs['Base Color']
                node_tree.links.new(image_texture_node.outputs['Color'], base_color_input)


    else:
        print("OBJECT HAS NOT MATERIAL")
    
    bpy.context.scene.exportState = False

    










