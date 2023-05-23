import bpy
from bpy.props import *
from bpy.types import Panel
from bpy.types import Menu
from . import functions

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
        row.operator("object.updatemesh",icon="MESH_CUBE")
        row.scale_y = 2
        row = layout.row()
        row.operator("object.creatematerial",icon="SHADING_RENDERED")
        row.scale_y = 2
        row = layout.row()
        row.separator()
        row = layout.row()
        row.label(text="Development",icon ="TOOL_SETTINGS")
        row.scale_y = 1.25
        row = layout.row()
        row.operator("object.exportupdates",icon="FILE_REFRESH")
        row.scale_y = 2
        row = layout.row()
        row.operator("object.exportfullscene",icon="SCENE_DATA")
        row.scale_y = 2
        row = layout.row()
        row.operator("object.exportfullcomp",icon="MESH_UVSPHERE")
        row.scale_y = 2
        row = layout.row()
        row.separator()
        row = layout.row()
        row.label(text="Preview",icon ="RESTRICT_RENDER_OFF")
        row.scale_y = 1.25
        row = layout.row()
        row.operator("object.chromepreview",icon='URL')
        row.scale_y = 2
        row = layout.row()
        row.separator()
        row = layout.row()
        row.label(text="Documentation",icon ="DOCUMENTS")
        row.scale_y = 1.25
        row = layout.row()
        row.operator("object.docs",icon='URL')
        row.scale_y = 2
        

    def menu_draw(self, context):
        layout = self.layout
        row = layout.row()
        row.scale_x = 1.1
        row.menu("TOPBAR_MT_custom_menu",icon="HIDE_OFF")

class TBA_INFO_PANEL(bpy.types.Panel):
    bl_label = "UNSEEN EXPORTER INFO"
    bl_idname = "OBJECT_PT_info"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "UNSEEN INFO"

    def draw(self, context):
        layout = self.layout
        count = str(bpy.context.scene.obCount)
        totalTex = str(bpy.context.scene.totalTex)
        size = str(functions.crd(bpy.context.scene.fileSize,3))
        row = layout.row()   
        row.label(text="Export Summary")
        row.scale_y = 1.25
        row = layout.row()  
        row.label(text="Objects: "+count)
        row.scale_y = 1
        row = layout.row()  
        row.label(text="Textures: "+totalTex)
        row.scale_y = 1
        row = layout.row()  
        row.label(text="Total Size: "+size+" MB")
        row.scale_y = 1


