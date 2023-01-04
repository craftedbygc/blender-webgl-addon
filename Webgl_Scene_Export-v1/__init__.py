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
    "name" : "Blender Webgl Exporter",
    "author" : "Tiago Andrade",
    "description" : "",
    "blender" : (3, 4, 0),
    "version" : (1, 0, 0),
    "location" : "Topbar",
    "warning" : "",
    "category" : "Object"
}

import bpy

#------------ SPACER ---------------------

#Import classes
from .op import (TBA_OT_export_scene,TBA_OT_export_comp_scene,TBA_OT_save_dialog,TBA_OT_open_chrome_preview)
from .ui import (TOPBAR_MT_custom_menu)           

#Classes list for register
#List of all classes that will be registered
classes = (TBA_OT_export_scene, TOPBAR_MT_custom_menu,TBA_OT_export_comp_scene,TBA_OT_save_dialog,TBA_OT_open_chrome_preview)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_custom_menu.menu_draw)

    #------------ SPACER ---------------------

    des = "Folder path to export scene assets to"
    bpy.types.Scene.saveFolderPath = bpy.props.StringProperty(name="", description=des, default="Set Path To Folder", subtype = 'DIR_PATH')

    des = "Define precision of data file - higher values will increase the data file size but match position better"
    bpy.types.Scene.precision = bpy.props.IntProperty(name="",description=des,default=4)

    des = "Remove indentation from export"
    bpy.types.Scene.minify = bpy.props.BoolProperty(name="Minify",description=des, default = True)

    des = "Website Preview Version Is Open - Untick if you need open a new tab and Preview Scene Site Again"
    bpy.types.Scene.previewOn = bpy.props.BoolProperty(name="Site Preview On",description=des, default = False)

    #------------ SPACER ---------------------



def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_custom_menu.menu_draw)
    for cls in classes:
        bpy.utils.unregister_class(cls)

    #------------ SPACER ---------------------  
    
    del bpy.types.Scene.saveFolderPath
    del bpy.types.Scene.precision
    del bpy.types.Scene.minify
    del bpy.types.Scene.previewOn




if __name__ == "__main__":
    register()