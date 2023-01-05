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

def findObject(obName):
    for ob in bpy.data.objects:
        if (ob.name == obName):
            return ob

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


def pollcheckExport():
    check = ["Scene Objects","Scene Instances"]
    for name in check:
        coll = findCollection(name)
        collName = coll.name
        path = bpy.context.scene.saveFolderPath
        #!= 0 and path !="Set Folder Path" and path !=""
        if(name == collName and len(coll.objects) != 0 and path !=""):
            return True
       
        return False    

#------------ SPACER ---------------------

def namingConvention(string):
    string = string.lower()
    string = string.replace(".", "-")
    return string

#------------ SPACER ---------------------

def geoCleaner(ob):
    forceselect(ob)
    bpy.ops.object.shade_smooth()
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles()
    bpy.ops.mesh.average_normals(average_type='FACE_AREA')
    bpy.ops.object.editmode_toggle()


def getunic(mylist):
    seen = set()
    dupes = [x for x in mylist if x in seen or seen.add(x)]  
    srtDupes = sorted(list(set(dupes)))
    return srtDupes


#------------ SPACER ---------------------
def getAniAtt(cam):
    sce = bpy.data.scenes["Scene"]
    frame_start = sce.frame_start
    frame_end = sce.frame_end
    #------------ SPACER ---------------------
    camLens = []
    cam_stops = []
    tgt_stops = []
    #------------ SPACER ---------------------
    for f in range(frame_start, frame_end+1):
        sce.frame_set(f)
        getCamStop = bpy.data.objects["cam_pos"].constraints["Follow Path"].offset_factor
        getTgtStop = bpy.data.objects["cam_tgt"].constraints["Follow Path"].offset_factor
        getLens = cam.lens
        cam_stops.append(getCamStop)
        tgt_stops.append(getTgtStop)
        camLens.append(getLens)
    
    cam_stops = getunic(cam_stops)
    tgt_stops = getunic(tgt_stops)
    camLens = getunic(camLens)
    
    return cam_stops, tgt_stops, camLens


#------------ SPACER ---------------------
def getPathPoints(ob):
    for subcurve in ob.data.splines:
        curvetype = subcurve.type
        points = []
        #------------------------
        if curvetype == 'NURBS':
            count = 0
            for nurbspoint in subcurve.points:
                points.append([rd(nurbspoint.co[0]),rd(nurbspoint.co[2]),-rd(nurbspoint.co[1])])
                count += 1 
        #------------------------  
        if curvetype == 'BEZIER':
            count = 0  
            for bezpoint in subcurve.bezier_points:
                points.append([rd(bezpoint.co[0]),rd(bezpoint.co[2]),-rd(bezpoint.co[1])])
                count += 1  

    return points




    
        


    



