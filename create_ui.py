import bpy
from bpy.props import *
from bpy.types import Panel
from bpy.types import Menu

class TOPBAR_MT_custom_menu(Menu):
    bl_label = "UNSEEN"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("wm.projectsettings",icon="SETTINGS")
        row.scale_y = 2
        row = layout.row()
        row.separator()
        row = layout.row()
        row.label(text="Design",icon ="SHADERFX")
        row.scale_y = 1.25
        row = layout.row()
        row.operator("object.update",icon="NODE_TEXTURE")
        row.scale_y = 2
        row = layout.row()
        row.separator()
        row = layout.row()
        row.label(text="Development",icon ="TOOL_SETTINGS")
        row.scale_y = 1.25
        row = layout.row()
        row.operator("object.exportscene",icon="SHADING_TEXTURE")
        row.scale_y = 2
        row = layout.row()
        row.operator("object.exportcompscene",icon="MESH_UVSPHERE")
        row.scale_y = 2
        row = layout.row()
        row.operator("object.chromepreview",icon='URL')
        row.scale_y = 2
        

    def menu_draw(self, context):
        layout = self.layout
        row = layout.row()
        row.scale_x = 1.1
        row.menu("TOPBAR_MT_custom_menu",icon="HIDE_OFF")
