import bpy
from bpy.types import Operator 
from . import functions
from . import batch_export
from . import set_data_file
from . import commads
from bpy.props import *
import webbrowser
from sys import platform

#------------ SPACER ---------------------

warn = "1 - If button is greyed out pls check scene structure or if all Projects Settings are defined!"
warn2 = "2 - If Site does not open pls uncheck the preview on option in Project Settings"
warn3 = "1- Npm Start runs once per blender session, so any issues restarting blender should help"

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
    bl_label ="Open Scene Preview"
    bl_description = "Opens Chrome Tab and Runs npm Start\n\n"+warn3

    @classmethod
    def poll(cls,context):
        return functions.pollcheckExport()

    def execute(self, context):
        #------------
        if(bpy.context.scene.previewOn == False):
            bpy.context.scene.previewOn = True
            #TBA STILL NOT WORKING
            commads.run()
        
        # url = 'http://localhost:3000/?gui'
        # if(platform == "darwin"):
        #     chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
        # else:
        #     chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
        # webbrowser.get(chrome_path).open(url)    
    
        return {"FINISHED"}

#------------ SPACER ---------------------