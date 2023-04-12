import bpy
from .create_op import TBA_OT_Update;
  

def update_tex_keymap():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(TBA_OT_Update.bl_idname, type='U', value='PRESS', shift=True)
        return km, kmi