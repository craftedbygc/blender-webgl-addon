import bpy
from mathutils import Quaternion
from mathutils import Euler
from . import functions

def find(depsgraph, evalOb, json):
    # Go through all the instances in the scene
    for instance in depsgraph.object_instances:
        # Get only the instances that are instanced on the evaluated object base.
        if instance.parent == evalOb:
            if instance.is_instance: # Check that it is in fact an instance
                obj = instance.object # This is the original object that is instanced.
                insname = functions.namingConvention(obj.name) # Match the name of the instanced geometry to the JSON structure
                # Grab data from the instance
                data = create(instance)
                if(insname in json):
                    json[insname].append(data)
                else:
                    print(f"NO JSON OBJECT FOR INSTANCE {insname}")
                   
def create(instance):
    data = []
    
    # Get the world matrix
    mat = instance.matrix_world
    # extract components back out of the matrix as two vectors and a quaternion
    pos, quat, sca = mat.decompose()
    
    pos = [functions.rd(pos.x),functions.rd(pos.z),functions.rd(-pos.y)]
    data.append(pos)

    quat.normalize()
    rot = Quaternion((quat[0], quat[1], quat[3], -quat[2]))
    rot = [functions.rd(rot[1]), functions.rd(rot[2]), functions.rd(rot[3]), functions.rd(rot[0])]
    data.append(rot)
    
    sca = [functions.rd(sca.x),functions.rd(sca.z),functions.rd(sca.y)]  
    data.append(sca)

    return data