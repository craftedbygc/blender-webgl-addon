import bpy
from bpy.props import *


class TOPBAR_MT_custom_menu(bpy.types.Menu):
    bl_label = "UNSEEN"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("wm.projectsettings",icon="SETTINGS")
        row.scale_y = 1.75
        row = layout.row()
        row.operator("object.exportscene",icon="SHADING_RENDERED")
        row.scale_y = 1.75
        row = layout.row()
        row.operator("object.exportcompscene",icon="MESH_UVSPHERE")
        row.scale_y = 1.5
        row = layout.row()
        row.operator("object.chromepreview",icon='URL')
        row.scale_y = 1.5

    def menu_draw(self, context):
        layout = self.layout
        row = layout.row()
        row.scale_x = 1.1
        row.menu("TOPBAR_MT_custom_menu",icon="HIDE_OFF")
