import bpy
from bpy.types import Operator 
from . import functions
from . import export_batch
from . import export_scene
from . import set_data_file
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
        #this export objects to glb
        #export_batch.glbExp(draco=False,material=True)
        #export the data
        #set_data_file.exportData()
        export_scene.main_scene_export(draco=False,material=True)
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
        #export_batch.glbExp(draco=False,material=False)
        #set_data_file.exportData()
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
        #export_batch.glbExp(draco=True,material=False)
        #set_data_file.exportData()
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
    bl_description = "Will update all the textures in created materials\n\n"+warn4

    @classmethod
    def poll(cls,context):
        return functions.pollcheckExport()

    def execute(self, context):
        functions.reload_textures()
        return {"FINISHED"}
    

#------------ SPACER ---------------------


class TBA_OT_ProgressPopUp(Operator):
    bl_idname = "object.simple_popup"
    bl_label = "Progress Pop Up"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        global message
        layout = self.layout
        layout.label(text=message)
        layout.operator("myops.simple_popup_close", text="Close")