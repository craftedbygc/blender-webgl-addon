import bpy
from bpy.props import *
from bpy.types import Panel
from bpy.types import Menu
from . import addon_updater_ops


class TBA_PT_AutoUpdater(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "TBA AUTO UPDATER"
    bl_category = "TBA-AUP"
    
    def draw(self, context):
        layout = self.layout
        addon_updater_ops.check_for_update_background()
        addon_updater_ops.update_notice_box_ui(self, context)




class TOPBAR_MT_custom_menu(Menu):
    bl_label = "UNSEEN"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Version 1.1.4",icon ="CONSOLE")
        row.scale_y = 1.25
        row = layout.row()
        row.operator("wm.projectsettings",icon="SETTINGS")
        row.scale_y = 1.75
        row = layout.row()
        row.separator()
        row = layout.row()
        row.label(text="Design",icon ="SHADERFX")
        row.scale_y = 1.25
        row = layout.row()
        row.operator("object.chromepreview",icon='URL')
        row.scale_y = 1.5
        row = layout.row()
        row.separator()
        row = layout.row()
        row.label(text="Development",icon ="TOOL_SETTINGS")
        row.scale_y = 1.25
        row = layout.row()
        row.operator("object.exportscenematerials",icon="SHADING_TEXTURE")
        row.scale_y = 1.75
        row = layout.row()
        row.operator("object.exportscene",icon="SHADING_RENDERED")
        row.scale_y = 1.75
        row = layout.row()
        row.operator("object.exportcompscene",icon="MESH_UVSPHERE")
        row.scale_y = 1.5
        

    def menu_draw(self, context):
        layout = self.layout
        row = layout.row()
        row.scale_x = 1.1
        row.menu("TOPBAR_MT_custom_menu",icon="HIDE_OFF")
