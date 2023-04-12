import bpy
import os
from . import functions


def set_image(folder_path,ob,img,socket_name):
    if socket_name:
        new_name = ob.name +"-"+socket_name 
    else:
        print(ob.name," - texture not connected to socket")
        
    covName = functions.namingConvention(new_name)
    file_name = covName + ".png"
    new_file_path = os.path.join(folder_path,file_name)
    print(new_file_path)
    img.filepath_raw = new_file_path
    img.file_format = 'PNG'
    img.save()


def export(folder_path,ob):
    if ob is not None and ob.type == "MESH":
        print("TBA-LEVEL-1")
        if len(ob.material_slots) > 0:
            mat = ob.material_slots[0].material
            if mat.use_nodes:
                for node in mat.node_tree.nodes:
                    if node.type == "TEX_IMAGE":
                        img = node.image
                        if img is not None:
                            socket_name = None
                            for link in mat.node_tree.links:
                                if link.to_node.type == "BSDF_PRINCIPLED" and link.from_node == node:
                                    socket_name = link.to_socket.name
                                    set_image(folder_path,ob,img,socket_name)
                                if link.to_node.type == "NORMAL_MAP" and link.from_node == node:
                                    socket_name = "normal"
                                    set_image(folder_path,ob,img,socket_name)

                                    
            
        else:
            print(ob.name,"NO MATERIAL DEFINED")




     


