import bpy
import os
from . import functions


def export(folder_path,ob):
    texObject = None
    matSettingsObject = None
    if ob is not None and ob.type == "MESH":
        if len(ob.material_slots) > 0:
            mat = ob.material_slots[0].material
            try:
                mat.use_nodes
            except:
                print('NO NODES USED')   

            if mat.use_nodes:
                #Create the texture object to save the file name too
                texObject = {}
                matSettingsObject = {}
                mat.name = ob.name + "-active-mat"
                for node in mat.node_tree.nodes:
                    if node.type == "TEX_IMAGE":
                        img = node.image
                        original_image = img
                        original_image_path = img.filepath
                        if img is not None and len(img.pixels) > 0:
                            socket_name = None
                            for link in mat.node_tree.links:
                                if link.to_node.type == "BSDF_DIFFUSE" and link.from_node == node:
                                    custom = node.label
                                    socket_name = custom
                                    socket_name = functions.namingConvention(socket_name)
                                    tex = set_image(folder_path,ob,img,socket_name)
                                    texObject[socket_name] = tex
                                    node.image = original_image
                                    node.image.filepath = original_image_path
                                if link.to_node.type == "BSDF_PRINCIPLED" and link.from_node == node:
                                    socket_name = functions.namingConvention(link.to_socket.name)
                                    tex = set_image(folder_path,ob,img,socket_name)
                                    texObject[socket_name] = tex
                                    node.image = original_image
                                    node.image.filepath = original_image_path 
                                if link.to_node.type == "NORMAL_MAP" and link.from_node == node:
                                    socket_name = "normal"
                                    tex = set_image(folder_path,ob,img,socket_name)
                                    texObject[socket_name] = tex
                                    node.image = original_image
                                    node.image.filepath = original_image_path
                        else:
                            print(ob.name,"NO IMAGE DATA TO EXPORT")

                    if node.type == "BSDF_PRINCIPLED":
                        setlist = ("Roughness","Metallic","Emission Strength")
                        for set in setlist:
                            val = node.inputs[set].default_value
                            set = functions.namingConvention(set)
                            matSettingsObject[set] = val
                return texObject, matSettingsObject
            
        else:
            print(ob.name,"NO MATERIAL DEFINED")
            return texObject, matSettingsObject


#------------ SPACER ---------------------
#------------ SPACER ---------------------
#------------ SPACER ---------------------

     
def set_image(folder_path,ob,img,socket_name):
    width, height = img.size
        
    folder_path = os.path.join(folder_path, "textures")

    if ob is not None:
        if socket_name:
            new_name = ob.name +"-"+ socket_name 
        else:
            print(ob.name," - texture not connected to socket")
    else: 
       new_name = socket_name

        
    covName = functions.namingConvention(new_name)
    file_name = covName + ".png"
    new_file_path = os.path.join(folder_path,file_name)

    new_img = img
    new_img.name = new_name
    
    if "envmap" in socket_name:
        tex_size = 2048
        scale_factor = tex_size/new_img.size[0]
        new_img.scale(tex_size,int(new_img.size[1]*scale_factor))

    if width > 2048 and "envmap" not in socket_name:
        tex_size = 2048
        new_img.scale(tex_size,tex_size)

    new_img.filepath_raw = new_file_path
    new_img.file_format = 'PNG'
    new_img.save()
    
    return file_name


def exportWorld(folder_path,sceneName):
    world = bpy.context.scene.world

    try:
        world.use_nodes
    except:
        print('NO NODES USED') 
            
    if world and world.use_nodes:
        texObject = {}
        matSettingsObject = {}
        check = bpy.context.scene.custEnvMap
        for node in world.node_tree.nodes:
            if node.type == "TEX_ENVIRONMENT":
                img = node.image
                original_image = img
                original_image_path = img.filepath
                if img is not None and len(img.pixels) > 0:
                    socket_name = None
                    for link in world.node_tree.links:
                        if link.to_node.type == "BACKGROUND" and link.from_node == node:
                            #Create a custom enviroment map
                            socket_name = "envmap"
                            if check:
                                socket_name = socket_name +'-'+ sceneName

                            ob = None
                            tex = set_image(folder_path,ob,img,socket_name)
                            texObject[socket_name] = tex
                            node.image = original_image
                            node.image.filepath = original_image_path 
                else:
                    print("NO WORLD IMAGE DATA TO EXPORT")
            if node.type == "BACKGROUND":
                set = "Strength"
                val = node.inputs[set].default_value
                set = functions.namingConvention(set)
                matSettingsObject[set] = val
        return texObject, matSettingsObject

    else:
        print("NO WORLD MATERIAL DEFINED")
        return texObject, matSettingsObject


