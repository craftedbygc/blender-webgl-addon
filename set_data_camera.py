import bpy
from mathutils import Quaternion
from . import functions

def create(camJsonObject,coll):

    #Objects needed
    names = ("cam_pos","cam_tgt","Camera")
    cam = bpy.data.cameras["Camera"]
    objects = functions.findObjects(names)

    camLens = functions.getAnimationValues(cam,type="float",prop="lens")
    print("HERE_camLens",camLens)
    camFilm = cam.sensor_width
    
    uimarkers = functions.getAnimationValues(cam,type="float",prop="UI Markers")
    keystops = functions.getAnimationValues(cam,type="float",prop="Key Stops")



    camJsonObject["focal-length"] = camLens
    camJsonObject["film-gauge"] = camFilm
    camJsonObject["ui-markers"] = uimarkers
    camJsonObject["key-stops"] = keystops



    if bpy.context.scene.camPaths:
        cpath = functions.findObject("cam-path")
        tpath = functions.findObject("tgt-path")  
        
        if names[0] in bpy.data.objects:
            cam_marker = functions.getAnimationValues(bpy.data.objects[names[0]],type="float",prop="constraints['Follow Path'].offset_factor")
            camJsonObject["cam-marker"] = cam_marker
        if names[1] in bpy.data.objects:
            tgt_marker = functions.getAnimationValues(bpy.data.objects[names[1]],type="float",prop="constraints['Follow Path'].offset_factor")
            camJsonObject["tgt-marker"] = tgt_marker
        
        if names[2] in bpy.data.objects:
            ui_marker = functions.getAnimationValues(bpy.data.objects[names[2]],type="float",prop="constraints['Follow Path'].offset_factor")
            camJsonObject["ui-marker"] = ui_marker

        if names[3] in bpy.data.objects:
            stops_marker = functions.getAnimationValues(bpy.data.objects[names[2]],type="float",prop="constraints['Follow Path'].offset_factor")
            camJsonObject["stops-marker"] = stops_marker

        camJsonObject["cam-path"] = functions.getPathPoints(cpath)
        camJsonObject["tgt-path"] = functions.getPathPoints(tpath)

    else:
        cam_pos = functions.getAnimationValues(objects[0],type="vector",prop="location")
        cam_tgt = functions.getAnimationValues(objects[1],type="vector",prop="location")
        camJsonObject["cam-positions"] = cam_pos
        camJsonObject["tgt-positions"] = cam_tgt
        
        if "cam_ui" in bpy.data.objects:
            ui_marker = functions.getAnimationValues(bpy.data.objects["cam_ui"],type="float",prop="constraints['Follow Path'].offset_factor")
            camJsonObject["ui-marker"] = ui_marker
        
        if "cam_stops" in bpy.data.objects:
            stops_marker = functions.getAnimationValues(bpy.data.objects["cam_stops"],type="float",prop="constraints['Follow Path'].offset_factor")
            camJsonObject["stops-marker"] = stops_marker

