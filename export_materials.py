import bpy
import os
import tempfile
from . import functions


#------------ SPACER ---------------------
#------------ SPACER ---------------------
#------------ SPACER ---------------------
def checkAndExport(folder_path,ob):
    bpy.context.view_layer.update()
    try:
        prop = functions.getproperty(ob,"updated")
    except:
        functions.createProp(ob,"updated",0)

    if prop>0:
        ob["updated"] = 1
        textures, matSettings = export(folder_path,ob)
        return textures, matSettings

        
def export(folder_path,ob):
    if ob is not None and ob.type == "MESH":
        if len(ob.material_slots) > 0:
            mat = ob.material_slots[0].material
            if mat.use_nodes:
                #Create the texture object to save the file name too
                texObject = {}
                matSettingsObject = {}
                for node in mat.node_tree.nodes:
                    if node.type == "TEX_IMAGE":
                        img = node.image
                        original_image = img
                        original_image_path = img.filepath
                        if img is not None and len(img.pixels) > 0:
                            socket_name = None
                            for link in mat.node_tree.links:
                                if link.to_node.type == "BSDF_PRINCIPLED" and link.from_node == node:
                                    socket_name = functions.namingConvention(link.to_socket.name)
                                    tex = set_image(folder_path,ob,img,socket_name)
                                    texObject[socket_name] = tex
                                    node.image = original_image
                                    node.image.filepath = original_image_path 
                                if link.to_node.type == "NORMAL_MAP" and link.from_node == node:
                                    socket_name = "normals"
                                    tex = set_image(folder_path,ob,img,socket_name)
                                    texObject[socket_name] = tex
                                    node.image = original_image
                                    node.image.filepath = original_image_path
                        else:
                            print(ob.name,"NO IMAGE DATA TO EXPORT")

                    if node.type == "BSDF_PRINCIPLED":
                        setlist = ("Roughness","Metallic","Emission Strength")
                        for set in setlist:
                            val = node.inputs["Roughness"].default_value
                            set = functions.namingConvention(set)
                            matSettingsObject[set] = val


                return texObject, matSettingsObject
            
        else:
            print(ob.name,"NO MATERIAL DEFINED")


#------------ SPACER ---------------------
#------------ SPACER ---------------------
#------------ SPACER ---------------------

     
def set_image(folder_path,ob,img,socket_name):
    
    folder_path =os.path.join(folder_path, "textures")
    
    if socket_name:
        new_name = ob.name +"-"+ socket_name 
    else:
        print(ob.name," - texture not connected to socket")
        
    covName = functions.namingConvention(new_name)
    file_name = covName + ".png"
    new_file_path = os.path.join(folder_path,file_name)
    print(new_file_path)

    # Save the original image to a temporary file
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
        temp_file_path = temp_file.name
        img.filepath_raw = temp_file_path
        img.file_format = 'PNG'
        img.save()
                            
    # Load the temporary file into a new image object
    new_img = bpy.data.images.load(temp_file_path)
    new_img.name = new_name
    
    new_img.scale(512,512)
    new_img.filepath_raw = new_file_path
    new_img.file_format = 'PNG'
    new_img.save()

    # Remove the temporary image from bpy.data.images
    bpy.data.images.remove(new_img)

    # Delete the temporary file
    os.remove(temp_file_path)

    

    return file_name
    
    

