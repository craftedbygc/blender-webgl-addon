import bpy
import time
import json
import math
import os
from mathutils import Quaternion

#------------ SPACER ---------------------

#Round Values
def rd(e):
    return round(e, bpy.context.scene.precision)

#------------ SPACER ---------------------

#Get a Property from an Object
def getproperty(object,property):
    check = True
    try:
        get = object[property]
    except:
        check = False
        
    if(check):
        if(object.type == 'MESH'):    
            value = rd(object[property])
        else:
            value = rd(object[property])
        
        return  value
    else:
        return False

#------------ SPACER ---------------------

#Force Select Objects
def forceselect(e):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = None
    e.select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[e.name]


#------------ SPACER ---------------------

#Force Objects to Be visible
def forceSelectable(e):
    coll = e.users_collection[0]
    collName = coll.name
    e.hide_select = False
    bpy.data.collections[collName].hide_select = False


#------------ SPACER ---------------------

def findCollection(collName):
    for coll in bpy.data.collections:
        if (coll.name == collName):
            return coll

#------------ SPACER ---------------------

def setFolderStructure():
        folderpath = bpy.context.scene.saveFolderPath
        folderName = "models"
        modelsFolder =os.path.join(folderpath, folderName)
        folderName = "texture"
        textFolder =os.path.join(folderpath, folderName)

        check = os.path.exists(modelsFolder)
        
        if(check == False):
            os.mkdir(modelsFolder)
            os.mkdir(textFolder)

#------------ SPACER ---------------------
    



