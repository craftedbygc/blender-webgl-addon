import bpy
from . import functions
from bpy.types import Object, Material

def check_and_change(ob,val):
    check = 'cam_' not in ob.name
    autoCheck = bpy.context.scene.exportState == False
    if ob.type == 'MESH' or ob.type == 'EMPTY':
        if ob.type != 'CURVE' and check and autoCheck:
            functions.createProp(ob,"updated",val)


def on_depsgraph_update(scene, depsgraph):
    for update in depsgraph.updates:
        if update.is_updated_shading:
            if isinstance(update.id, Material):
                material = update.id

                for ob in scene.objects:
                    if ob.type == 'MESH':
                        if material.name in ob.data.materials:
                            check_and_change(ob,2)

        if update.is_updated_transform or update.is_updated_geometry:
            if isinstance(update.id, Object):
                ob = bpy.data.objects[update.id.name]
                prop = functions.getproperty(ob,"updated")
                if prop is not None and prop < 1:
                    check_and_change(ob,1)