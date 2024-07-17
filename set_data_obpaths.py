import bpy
from mathutils import Quaternion
from . import functions

def create(jsonObject,ob):
    functions.forceselect(ob)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    name = ob.name
    name = name[:-5]
    name = functions.namingConvention(name)
    jsonObject[name] = []
    jsonObject[name].append(functions.getPathPoints(ob))

    # Get the paths' extra attributes
    jsonObject[name].append({})
    jsonObject[name][1]['attributes'] = {}

    # rootType = ob.get('rootType') # Get specific attribute example
    # if(rootType):
    #     jsonObject[name][1]['attributes']['rootType'] = rootType

    for K in ob.keys():
        if(K.startswith("custom")):
            custom_left_trimmed = K.lstrip('custom') # Remove the 'custom' prefix
            custom_left_trimmed = custom_left_trimmed[0].lower() + custom_left_trimmed[1:] # Lowercase the first letter
            attribute_value = ob[K]
            jsonObject[name][1]['attributes'][custom_left_trimmed] = attribute_value

    return {"FINISHED"}