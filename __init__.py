# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.



bl_info = {
    "name" : "Unseen BWE",
    "author" : "Tiago Andrade",
    "description" : "",
    "blender" : (3, 6, 1),
    "version" : (1, 9, 1),
    "location" : "Topbar",
    "warning" : "",
    "category" : "Object"
}

import bpy
from . import functions
from . import keymaps
from . import checkers
from . import export_scene
from bpy.app.handlers import persistent, depsgraph_update_post, depsgraph_update_pre


#------------ SPACER ---------------------
from . import external_addon_updater_ops
#from .set_addon_preferences import (DemoPreferences)

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
        ver = functions.tupleToString(bl_info["version"])
        blend = functions.tupleToString(bl_info["blender"])
        row.label(text="Addon v"+ver+" Installed",icon ="SCRIPT")
        row.scale_y = spacer*1
        row = layout.row()
        row.label(text="Blender v" +blend ,icon ="BLENDER")
        row.scale_y = spacer*1
        external_addon_updater_ops.check_for_update_background()
        external_addon_updater_ops.update_notice_box_ui(self, context,ver)
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
        row.scale_y = spacer*1
        #------------
        row = layout.row()
        row.label(text="Update Mesh Folder",icon ="FOLDER_REDIRECT")
        #------------
        row = layout.row()
        row.prop(sce,'updateMeshFolder')
        row.scale_y = 1.5
        #------------
        row = layout.row()
        row.label(text="")
        row.scale_y = spacer*1
        #------------
        row = layout.row()
        row.label(text="Materials Textures Folder",icon ="FOLDER_REDIRECT")
        #------------
        row = layout.row()
        row.prop(sce,'textureFolder')
        row.scale_y = 1.5
        #------------
        row = layout.row()
        row.label(text="")
        row.scale_y = spacer*1
        #------------
        row = layout.row()
        row.label(text="Data File Options",icon ="OPTIONS")
        #------------
        row = layout.row()
        row.label(text="")
        row.scale_y = spacer*0.15
        #------------
        row = layout.row()
        row.prop(sce,'precision')
        row.scale_y = 1
        #------------
        row = layout.row()
        row.prop(sce,'aniExport')
        row.scale_y = 1
        #------------
        row = layout.row()
        row.prop(sce,'camPaths')
        row.scale_y = 1
        #------------
        row = layout.row()
        row.prop(sce,'custEnvMap')
        row.scale_y = 1
        #------------
        row = layout.row()
        row.prop(sce,'minify')
        row.scale_y = 1
        #------------
        row = layout.row()
        row.prop(sce,'expOnSave')
        row.scale_y = 1
        #------------
        row = layout.row()
        row.prop(sce,'noMatExp')
        row.scale_y = 1
        #------------
        row = layout.row()
        row.prop(sce,'checkUpdates')
        row.scale_y = 1
        #------------
        row = layout.row()
        row.label(text="")
        row.scale_y = spacer*2


    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


#------------ SPACER ---------------------

#Import classes
from .create_op import TBA_OT_CreateMaterials,TBA_OT_UpdateMesh,TBA_OT_Docs,TBA_OT_INFO,TBA_OT_Update,TBA_OT_Export_Updates,TBA_OT_Export_Scene_Data,TBA_OT_Export_Scene_Plus_Textures,TBA_OT_Export_Draco_Comp,TBA_OT_open_chrome_preview
from .create_ui import TBA_INFO_PANEL,TOPBAR_MT_custom_menu         

#Classes list for register
#List of all classes that will be registered
classes = (TBA_OT_CreateMaterials,TBA_OT_UpdateMesh,TBA_OT_Docs,TBA_INFO_PANEL,TBA_OT_INFO,TBA_OT_Update,TOPBAR_MT_custom_menu,TBA_OT_Export_Scene_Data,TBA_OT_Export_Scene_Plus_Textures,TBA_OT_Export_Draco_Comp,TBA_OT_save_dialog,TBA_OT_open_chrome_preview,TBA_OT_Export_Updates)


#------------ SPACER ---------------------

addon_keymaps = []

#------------ SPACER ---------------------
# Set option to Update on save file
@persistent
def save_hanfler(dummy):
    check = functions.pollcheckExport() == True
    checkP = bpy.context.scene.expOnSave == True
    print("TBA_Before_Check")
    if(check and checkP):
        print("TBA_Auto_Save_On")
        functions.setFolderStructure()
        export_scene.main_scene_export(draco=False,fullScene = False)

#------------ Fetch Children Collections ---------------------


@persistent
def executeOnLoad(dummy):
    print("NEW SCENE - RESET UPDATE")
    #functions.restUpdateState()
    bpy.context.scene.previewOn = False
    depsgraph_update_post.append(checkers.on_depsgraph_update)
    external_addon_updater_ops.check_for_update_onload()


#------------ SPACER ---------------------


def register():
    #ADDON UPDATER CODE
    external_addon_updater_ops.register(bl_info)

    #------------ SPACER ---------------------
    #Register Addon Classes
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_custom_menu.menu_draw)
    
    #------------ SPACER ---------------------
    # Add the hotkey
    km,kmi = keymaps.update_tex_keymap()
    addon_keymaps.append((km, kmi))


    #------------ SPACER ---------------------

    des = "Folder path to export scene assets to"
    bpy.types.Scene.saveFolderPath = bpy.props.StringProperty(name="", description=des, default="", subtype = 'DIR_PATH')

    des = "Folder path to refresh objects"
    bpy.types.Scene.updateMeshFolder = bpy.props.StringProperty(name="", description=des, default="", subtype = 'DIR_PATH')

    des = "Folder path to incoming texture"
    bpy.types.Scene.textureFolder = bpy.props.StringProperty(name="", description=des, default="", subtype = 'DIR_PATH')

    des = "Define precision of data file - higher values will increase the data file size but match position better"
    bpy.types.Scene.precision = bpy.props.IntProperty(name="Precision",description=des,default=4)

    des = "Tick to use cam paths in the scene"
    bpy.types.Scene.camPaths = bpy.props.BoolProperty(name="Cam Paths",description=des, default = False)

    des = "Remove indentation from export"
    bpy.types.Scene.minify = bpy.props.BoolProperty(name="Minify",description=des, default = True)

    des = "Set Addon to export everytime you save the file"
    bpy.types.Scene.expOnSave = bpy.props.BoolProperty(name="Auto Export On Save",description=des, default = False)

    des = "Check If Objects were edited before export, improves performance"
    bpy.types.Scene.checkUpdates = bpy.props.BoolProperty(name="Export Only Edited Geometry",description=des, default = True)

    des = "Set this scene to export a custom enviroment map"
    bpy.types.Scene.custEnvMap = bpy.props.BoolProperty(name="Export Dedicated Enviroment Map",description=des, default = False)

    des = "No Material export"
    bpy.types.Scene.noMatExp = bpy.props.BoolProperty(name="No Material export",description=des, default = False)

    des = "If the assets are Animated it will export it"
    bpy.types.Scene.aniExport = bpy.props.BoolProperty(name="Animation Export",description=des, default = False)

    des = "Website Preview Version Is Open - Untick if you need open a new tab and Preview Scene Site Again"
    bpy.types.Scene.previewOn = bpy.props.BoolProperty(name="Site Preview On",description=des, default = False)
    
    des = "Folder path to export scene assets to"
    bpy.types.Scene.progressPopup = bpy.props.StringProperty(default="EXPORT STARTED")

    bpy.types.Scene.obCount = bpy.props.IntProperty(name="Exported Objects",description="Number of Exported Objects",default=0)

    bpy.types.Scene.totalTex = bpy.props.IntProperty(name="Exported Textures",description="Number of Exported Textures",default=0)
    
    bpy.types.Scene.fileSize = bpy.props.FloatProperty(name="File Size",description="Total File Size",default=0)

    bpy.types.Scene.exportState = bpy.props.BoolProperty(default = False)

    #------------ SPACER ---------------------

    if not save_hanfler in bpy.app.handlers.save_post:
        bpy.app.handlers.save_post.append(save_hanfler)
    if not executeOnLoad in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(executeOnLoad)

def unregister():
    external_addon_updater_ops.unregister()
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_custom_menu.menu_draw)
    #------------ SPACER ---------------------  
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    #------------ SPACER ---------------------  
    for cls in classes:
        bpy.utils.unregister_class(cls)

    #------------ SPACER ---------------------  
    if save_hanfler in bpy.app.handlers.save_post:
        bpy.app.handlers.save_post.remove(save_hanfler)
    if executeOnLoad in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(executeOnLoad)

    del bpy.types.Scene.saveFolderPath
    del bpy.types.Scene.updateMeshFolder
    del bpy.types.Scene.textureFolder
    del bpy.types.Scene.precision
    del bpy.types.Scene.minify
    del bpy.types.Scene.previewOn
    del bpy.types.Scene.expOnSave

if __name__ == "__main__":
    register()