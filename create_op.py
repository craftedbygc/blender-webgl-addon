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

class TBA_OT_Export_Updates(Operator):
    bl_idname = "object.exportupdates"
    bl_label ="Export Updates"
    bl_description = "Export UpdatesUncompreesed With Materials \n\n"+warn

    @classmethod
    def poll(cls,context):
        return functions.pollcheckExport()

    def execute(self, context):
        functions.setFolderStructure()
        export_scene.main_scene_export(draco=False,fullScene = False)
        return {"FINISHED"}
    
#------------ SPACER ---------------------

class TBA_OT_Export_Full_Scene(Operator):
    bl_idname = "object.exportfullscene"
    bl_label ="Export Full Scene"
    bl_description = "Export Scene Uncompressed With Materials\n\n"+warn

    @classmethod
    def poll(cls,context):
        return functions.pollcheckExport()

    def execute(self, context):
        functions.setFolderStructure()
        export_scene.main_scene_export(draco=False,fullScene = True)
        return {"FINISHED"}

#------------ SPACER ---------------------

class TBA_OT_Export_Full_Comp(Operator):
    bl_idname = "object.exportfullcomp"
    bl_label ="Export Full Draco Scene"
    bl_description = "Export Scene With Draco Compression \n\n"+warn

    @classmethod
    def poll(cls,context):
        return functions.pollcheckExport()

    def execute(self, context):
        functions.setFolderStructure()
        export_scene.main_scene_export(draco=False,fullScene = True)
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


#------------ SPACER ---------------------
class TBA_OT_UpdateMesh(Operator):
    bl_idname = "object.updatemesh"
    bl_label ="Update Object"
    bl_description = "Update Selected Object"

    @classmethod
    def poll(cls,context):
        return functions.pollcheckExport()

    def execute(self, context):
        export_import.update_mesh()
        return {"FINISHED"}
    
#------------ SPACER ---------------------
class TBA_OT_CreateMaterials(Operator):
    bl_idname = "object.creatematerial"
    bl_label ="Create Materials"
    bl_description = "Create Materials based on the textures available on the texture folder"

    @classmethod
    def poll(cls,context):
        return functions.pollcheckExport()

    def execute(self, context):
        export_import.update_create_material()
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
    

class TBA_OT_Docs(Operator):
    bl_idname = "object.docs"
    bl_label ="Open Notion Docs"
    bl_description = "Documentation on the use of the Addon"

    @classmethod
    def poll(cls,context):
        return functions.pollcheckExport()

    def execute(self, context):
        functions.openDocumentation()
        return {"FINISHED"}



    