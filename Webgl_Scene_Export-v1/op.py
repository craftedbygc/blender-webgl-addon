import bpy
from bpy.types import Operator 
from . import functions
from . import batch_export
from . import set_data_file
from bpy.props import *
import webbrowser
from sys import platform

#------------ SPACER ---------------------

class TBA_OT_save_dialog(bpy.types.Operator):
    bl_label = "Projects Settings"
    bl_idname = "wm.projectsettings"

    def execute(self, context):
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        sce = context.scene
        spacer = 1
        #------------
        row = layout.row()
        row.label(text="")
        row.scale_y = spacer*0.5
        #------------
        row = layout.row()
        row.label(text="Save To Folder",icon ="FOLDER_REDIRECT")
        #------------
        row = layout.row()
        row.prop(sce,'saveFolderPath')
        row.scale_y = 1.5
        #------------
        row = layout.row()
        row.label(text="")
        row.scale_y = spacer*0.5
        #------------
        row = layout.row()
        row.label(text="Precision",icon ="VIEWZOOM")
        #------------
        row = layout.row()
        row.prop(sce,'precision')
        row.scale_y = 1.5
        #------------
        row = layout.row()
        row.label(text="")
        row.scale_y = spacer*0.5
        #------------
        row = layout.row()
        row.label(text="Data File Options",icon ="OPTIONS")
        #------------
        row = layout.row()
        row.prop(sce,'minify')
        row.prop(sce,'previewOn')
        row.scale_y = 1.5
        #------------
        row = layout.row()
        row.label(text="")
        row.scale_y = spacer*3

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

#------------ SPACER ---------------------

class TBA_OT_export_scene(Operator):
    bl_idname = "object.exportscene"
    bl_label ="Export Scene"
    bl_description = "Export All Scene"

    def execute(self, context):
        functions.setFolderStructure()
        batch_export.glbExp(draco=False,material=False)
        set_data_file.exportData()
        return {"FINISHED"}

#------------ SPACER ---------------------

class TBA_OT_export_comp_scene(Operator):
    bl_idname = "object.exportcompscene"
    bl_label ="Export Scene Draco Compressed"
    bl_description = "Export Scene With Draco Compression"

    def execute(self, context):
        functions.setFolderStructure()
        batch_export.glbExp(draco=True,material=False)
        set_data_file.exportData()
        return {"FINISHED"}

#------------ SPACER ---------------------

class TBA_OT_open_chrome_preview(Operator):
    bl_idname = "object.chromepreview"
    bl_label ="Preview Scene Site"
    bl_description = "Export and Preview Scene With Materials"

    def execute(self, context):
        functions.setFolderStructure()
        batch_export.glbExp(draco=False,material=False)
        set_data_file.exportData()
        #------------
        if(bpy.context.scene.previewOn == False):

            bpy.context.scene.previewOn = True

            url = 'http://localhost:3000/'
            if(platform == "darwin"):
                chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
            else:
                chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
            webbrowser.get(chrome_path).open(url)
        return {"FINISHED"}

#------------ SPACER ---------------------