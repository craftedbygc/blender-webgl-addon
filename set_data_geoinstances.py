import bpy
from . import functions

def find(sceneCol, jsonObject):

    # Insert other code here
    
    if(collmain):
                # Get evaluated dependency graph of the scene ===================================== #
                depsgraph = bpy.context.evaluated_depsgraph_get()
                bpy.data.collections[collName].color_tag = 'COLOR_05' # Set the colour
                # Go through all subcollections in the Instances collection
                for coll in collmain.children:
                        bpy.data.collections[coll.name].color_tag = 'COLOR_04'
                        
                        # cName = coll.name # Get the name of the instance collection, not needed
                        
                        myList = [obj.name for obj in coll.all_objects] # Get a list of all objects in the collection
                        myList = sorted(myList)
                        # Go through all objects
                        for name in myList:
                            ob = coll.all_objects[name] # Get the base object on which there's instances
                            # Get the object in the evaluated dependency graph to attach instances
                            evalOb = ob.evaluated_get(depsgraph)
                            
                            # Go through all the instances in the scene
                            for object_instance in depsgraph.object_instances:
                                # Get only the instances that are instanced on the object in the collection.
                                if object_instance.parent == evalOb:
                                    
                                    obj = object_instance.object # This is the original object that is instanced.
                                    
                                    instance_name = obj.name # Get the name of the instanced geometry
                                    instName = functions.namingConvention(instance_name)
                                    
                                    # Save per instance geometry
                                    if instName not in jsonObject["instances"]:
                                        jsonObject["instances"][instName] = [] # Save per type of object that's instanced
                                    
                                    if object_instance.is_instance: # Check that it is an instance
                                        create(jsonObject["instances"], object_instance, instance_name, False) # Save per instance object 



def create(objects, instance, name, check = bool):
            data = []
            
            # Get the world matrix
            mat = instance.matrix_world
            # extract components back out of the matrix as two vectors and a quaternion
            pos, rot, sca = mat.decompose()
            
            pos = [rd(pos.x),rd(pos.z),rd(-pos.y)]
            data.append(pos)
            
            rot = [rd(rot[1]), rd(rot[2]), rd(rot[3]), rd(rot[0])]
            data.append(rot)
            
            sca = [rd(sca.x),rd(sca.y),rd(sca.z)]  
            data.append(sca)
            
            # Get the UVs - optional
            uv = instance.uv
            
            objects[name].append(data)