TBA_Version = "1.2.3"

import bpy
from bpy.types import Operator 
from . import functions
from . import batch_export
from . import set_data_file
from bpy.props import *
import webbrowser
from sys import platform
from . import addon_updater_ops
#------------ SPACER ---------------------

class TBA_OT_save_dialog(bpy.types.Operator):
    bl_label = "Project Settings"
    bl_idname = "wm.projectsettings"

    def execute(self, context):
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        sce = context.scene
        spacer = 1
        #------------
        row = layout.row()
        row.label(text="Addon Updates",icon ="SCRIPT")
        addon_updater_ops.check_for_update_background()
        addon_updater_ops.update_notice_box_ui(self, context)
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
        row.label(text="Data File Options",icon ="OPTIONS")
        #------------
        row = layout.row()
        row.prop(sce,'precision')
        row.scale_y = 1.5
         #------------
        row = layout.row()
        row.prop(sce,'minify')
        row.scale_y = 1.5
        #------------
        row = layout.row()
        row.prop(sce,'previewOn')
        row.scale_y = 1.5
        #------------
        row = layout.row()
        row.prop(sce,'expOnSave')
        row.scale_y = 1.5
        #------------
        
        row = layout.row()
        row.label(text="")
        row.scale_y = spacer*2

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


warn = "1 - If button is greyed out pls check scene structure or if all Projects Settings are defined!"
warn2 = "2 - If Site does not open pls uncheck the preview on option in Project Settings"

class TBA_OT_export_scene_materials(Operator):
    bl_idname = "object.exportscenematerials"
    bl_label ="Export With Materials"
    bl_description = "Export All Scene Uncompreesed And With Materials \n\n"+warn

    @classmethod
    def poll(cls,context):
        return functions.pollcheckExport()

    def execute(self, context):
        functions.setFolderStructure()
        batch_export.glbExp(draco=False,material=True)
        set_data_file.exportData()
        return {"FINISHED"}

#------------ SPACER ---------------------

class TBA_OT_export_scene(Operator):
    bl_idname = "object.exportscene"
    bl_label ="Export Uncompressed"
    bl_description = "Export Scene Uncompressed \n\n"+warn

    @classmethod
    def poll(cls,context):
        return functions.pollcheckExport()

    def execute(self, context):
        functions.setFolderStructure()
        batch_export.glbExp(draco=False,material=False)
        set_data_file.exportData()
        return {"FINISHED"}

#------------ SPACER ---------------------

class TBA_OT_export_comp_scene(Operator):
    bl_idname = "object.exportcompscene"
    bl_label ="Export Draco Compressed"
    bl_description = "Export Scene With Draco Compression \n\n"+warn

    @classmethod
    def poll(cls,context):
        return functions.pollcheckExport()

    def execute(self, context):
        functions.setFolderStructure()
        batch_export.glbExp(draco=True,material=False)
        set_data_file.exportData()
        return {"FINISHED"}

#------------ SPACER ---------------------

class TBA_OT_open_chrome_preview(Operator):
    bl_idname = "object.chromepreview"
    bl_label ="Preview Scene Online"
    bl_description = "Export and Preview Scene With Materials \n\n"+warn+"\n"+warn2

    @classmethod
    def poll(cls,context):
        return functions.pollcheckExport()

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