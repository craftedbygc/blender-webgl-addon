import bpy
import os
from . import functions


def export(folder_path,ob,prop):
    texObject = None
    matSettingsObject = None
    if ob is not None and ob.type == "MESH":
        if len(ob.material_slots) > 0:
            mat = ob.material_slots[0].material
            try:
                mat.use_nodes
            except:
                print('NO NODES USED')   

            if mat is not None and mat.use_nodes:
                #Create the texture object to save the file name too
                texObject = {}
                matSettingsObject = {}
                mat.name = ob.name + "-active-mat"
                for node in mat.node_tree.nodes:
                    if node.type == "TEX_IMAGE":
                        if node.image is not None and len(node.image.pixels) > 0:
                            img = node.image
                            original_image = img
                            original_image_path = img.filepath
                            print("original_image_path:",original_image_path)
                            socket_name = None
                            for link in mat.node_tree.links:
                                if link.to_node.type == "BSDF_PRINCIPLED" and link.from_node == node:
                                    socket_name = functions.namingConvention(link.to_socket.name)
                                    if node.image.source == 'TILED':
                                        print("TILED IMAGE:",socket_name)
                                        # Collect the UDIM tiles' file paths into a list
                                        udim_filepaths = []
                                        for tile in node.image.tiles:
                                            # Append the UDIM tile number to the socket name
                                            print("TILE NUMBDER",tile.number)
                                            tileNumber = tile.number
                                            tex = set_image(prop,folder_path, ob, img, socket_name,tiles = tileNumber)
                                            udim_filepaths.append(tex)
                                        texObject[socket_name] = udim_filepaths
                                    else:
                                        print("SIMPLE IMAGE:",socket_name)
                                        tex = set_image(prop,folder_path, ob, img, socket_name,tiles = None)
                                        texObject[socket_name] = tex
                                    node.image = original_image
                                    node.image.filepath = original_image_path
                                if link.to_node.type == "NORMAL_MAP" and link.from_node == node:
                                    socket_name = "normal"
                                    if node.image.source == 'TILED':
                                        print("TILED IMAGE:",socket_name)
                                        # Collect the UDIM tiles' file paths into a list
                                        udim_filepaths = []
                                        for tile in node.image.tiles:
                                            # Append the UDIM tile number to the socket name
                                            print("TILE NUMBDER",tile.number)
                                            tileNumber = tile.number
                                            tex = set_image(prop,folder_path, ob, img, socket_name,tiles = tileNumber)
                                            udim_filepaths.append(tex)
                                        texObject[socket_name] = udim_filepaths
                                    else:
                                        print("SIMPLE IMAGE:",socket_name)
                                        tex = set_image(prop,folder_path, ob, img, socket_name,tiles = None)
                                        texObject[socket_name] = tex
                                    node.image = original_image
                                    node.image.filepath = original_image_path
                                if link.to_node.type == "BSDF_DIFFUSE" and link.from_node == node:
                                    custom = node.label
                                    socket_name = custom
                                    socket_name = functions.namingConvention(socket_name)
                                    if node.image.source == 'TILED':
                                        print("TILED IMAGE:",socket_name)
                                        # Collect the UDIM tiles' file paths into a list
                                        udim_filepaths = []
                                        for tile in node.image.tiles:
                                            # Append the UDIM tile number to the socket name
                                            print("TILE NUMBDER",tile.number)
                                            tileNumber = tile.number
                                            tex = set_image(prop,folder_path, ob, img, socket_name,tiles = tileNumber)
                                            udim_filepaths.append(tex)
                                        texObject[socket_name] = udim_filepaths
                                    else:
                                        print("SIMPLE IMAGE:",socket_name)
                                        tex = set_image(prop,folder_path, ob, img, socket_name,tiles = None)
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

     
def set_image(prop,folder_path,ob,img,socket_name,tiles):
    width, height = img.size
        
    folder_path = os.path.join(folder_path, "textures")

    if ob is not None:
        if socket_name:
            obNameCorrect = functions.namingConvention(ob.name)
            if tiles is not None:
                jsonName = obNameCorrect +"-"+ socket_name + "." + "<UDIM>" + ".png"
                file_name = obNameCorrect +"-"+ socket_name + "." + f"{tiles}" + ".png"
                new_file_path = os.path.join(folder_path,jsonName)
                mat = ob.material_slots[0].material
                nodes = mat.node_tree.nodes
                
            else:
                file_name = obNameCorrect +"-" + socket_name+".png"
                new_file_path = os.path.join(folder_path,file_name)
                new_img = img
                new_img.name = file_name
                
        else:
            print(ob.name," - texture not connected to socket")
    else: 
       file_name = socket_name + ".png"
       new_file_path = os.path.join(folder_path,file_name)
       
    if prop > 1:
        new_img = img
        #new_img.name = file_name
        
        if "envmap" in socket_name or "bgmap" in socket_name:
            tex_size = 2048
            scale_factor = tex_size/new_img.size[0]
            new_img.scale(tex_size,int(new_img.size[1]*scale_factor))

        if width > 2048 and ("envmap" not in socket_name and "bgmap" not in socket_name):
            tex_size = 2048
            new_img.scale(tex_size,tex_size)

        new_img.filepath_raw = new_file_path
        new_img.file_format = 'PNG'
        new_img.save()
    
    return file_name

 
def exportWorld(folder_path,sceneName,prop):
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
                            # Check if the background node's name is "BG"
                            print("TBA-NAME:",link.to_node.name)
                            if link.to_node.label == "BG":
                                print("TBA-FOUND CUSTOM BG")
                                #Create a custom enviroment map
                                socket_name = "bgmap"
                                if check:   
                                    socket_name = socket_name +'-'+ sceneName

                                ob = None
                                print("SIMPLE IMAGE:",socket_name)
                                tex = set_image(prop,folder_path, ob, img, socket_name,tiles = None)
                                texObject[socket_name] = tex
                                node.image = original_image
                                node.image.filepath = original_image_path
                            else:
                                #Create a custom enviroment map
                                socket_name = "envmap"
                                if check:   
                                    socket_name = socket_name +'-'+ sceneName

                                ob = None
                                print("SIMPLE IMAGE:",socket_name)
                                tex = set_image(prop,folder_path, ob, img, socket_name,tiles = None)
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


