import bpy
from mathutils import Quaternion
from . import functions

def create(jsonObject,ob):
    functions.forceselect(ob)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    name = ob.name
    name = name[:-5]
    name = functions.namingConvention(name)
    jsonObject[name] = functions.getPathPoints(ob)

    return {"FINISHED"}