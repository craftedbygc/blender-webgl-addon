import bpy
from . import functions
from bpy.types import Object, Material, World

def check_and_change(e,val):
    autoCheck = bpy.context.scene.exportState == False
    if isinstance(e, bpy.types.World):
        if autoCheck:
            functions.createWorldProp(e,"updated",val)
    else:
        check = 'cam_' not in e.name
        if e.type == 'MESH' or e.type == 'EMPTY':
            if e.type != 'CURVE' and check and autoCheck:
                functions.createProp(e,"updated",val)


def on_depsgraph_update(scene, depsgraph):
    for update in depsgraph.updates:
        if update.is_updated_shading:
            if isinstance(update.id, World):
                world = bpy.context.scene.world
                check_and_change(world,2)

            if isinstance(update.id, Material):
                material = update.id
                for ob in scene.objects:
                    if ob.type == 'MESH':
                        if material.name in ob.data.materials:
                            print("MATERIAL:",material.name)
                            check_and_change(ob,2)
                            
        if update.is_updated_transform or update.is_updated_geometry:
            if isinstance(update.id, Object):
                ob = bpy.data.objects[update.id.name]
                prop = functions.getproperty(ob,"updated")
                if prop is not None and prop < 1:
                    check_and_change(ob,1)