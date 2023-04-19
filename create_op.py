import bpy
import time
from bpy.types import Operator 
from . import functions
from . import export_import
from . import export_scene
from . import baking_textures
from . import commads
from bpy.props import *
import webbrowser
from sys import platform

#------------ SPACER ---------------------

warn = "1 - If button is greyed out pls check scene structure or if all Projects Settings are defined!"
warn2 = "2 - If Site does not open pls uncheck the preview on option in Project Settings"
warn3 = "1- Npm Start runs once per blender session, so any issues restarting blender should help"
warn4 = "1- You can also use the shift+U shortcut to perfome this operation"

class TBA_OT_export_scene_materials(Operator):
    bl_idname = "object.exportscenematerials"
    bl_label ="Export With Materials"
    bl_description = "Export All Scene Uncompreesed And With Materials \n\n"+warn

    @classmethod
    def poll(cls,context):
        return functions.pollcheckExport()

    def execute(self, context):
        functions.setFolderStructure()
        export_scene.main_scene_export(draco=False)
        return {"FINISHED"}
    
#------------ SPACER ---------------------

class TBA_OT_export_scene(Operator):
    bl_idname = "object.exportscene"
    bl_label ="Export Uncompressed & Materials"
    bl_description = "Export Scene Uncompressed \n\n"+warn

    @classmethod
    def poll(cls,context):
        return functions.pollcheckExport()

    def execute(self, context):
        functions.setFolderStructure()
        export_scene.main_scene_export(draco=False)
        return {"FINISHED"}

#------------ SPACER ---------------------

class TBA_OT_export_comp_scene(Operator):
    bl_idname = "object.exportcompscene"
    bl_label ="Export Draco Compressed & Materials"
    bl_description = "Export Scene With Draco Compression \n\n"+warn

    @classmethod
    def poll(cls,context):
        return functions.pollcheckExport()

    def execute(self, context):
        functions.setFolderStructure()
        export_scene.main_scene_export(draco=False)
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

        commads.run()
        
        return {"FINISHED"}

#------------ SPACER ---------------------
class TBA_OT_Update(Operator):
    bl_idname = "object.update"
    bl_label ="Update Textures"
    bl_description = "If texture files have changed you can force update with this operation to reload all the texures used\n\n"+warn4

    @classmethod
    def poll(cls,context):
        return functions.pollcheckExport()

    def execute(self, context):
        functions.reload_textures()
        return {"FINISHED"}
    
class TBA_OT_Import_c4d(Operator):
    bl_idname = "object.importc4d"
    bl_label ="Import C4D Scene"
    bl_description = "Import C4D Scene\n\n"+warn

    @classmethod
    def poll(cls,context):
        return functions.pollcheckExport()

    def execute(self, context):
        functions.setFolderStructure()
        #baking_textures.bake_maps()
        return {"FINISHED"}
    

class TBA_OT_INFO(Operator):
    bl_idname = "object.info"
    bl_label ="Export Info"
    bl_description = "Info relating the exporting process"

    @classmethod
    def poll(cls,context):
        return functions.pollcheckExport()

    def execute(self, context):
        return {"FINISHED"}
    