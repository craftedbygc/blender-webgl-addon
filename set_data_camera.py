import bpy
from mathutils import Quaternion
from . import functions

def create(camJsonObject,coll):

    #Objects needed
    names = ("cam_pos","cam_tgt","Camera")
    cam = bpy.data.cameras["Camera"]
    objects = functions.findObjects(names)

    camLens = functions.getAnimationValues(cam,type="float",prop="lens")
    camFilm = cam.sensor_width

    camJsonObject["focal-length"] = camLens
    camJsonObject["film-gauge"] = camFilm

    if bpy.context.scene.camPaths:
        cpath = functions.findObject("cam-path")
        tpath = functions.findObject("tgt-path")  

        cam_stops = functions.getAnimationValues(bpy.data.objects[names[0]],type="float",prop="constraints['Follow Path'].offset_factor")
        tgt_stops = functions.getAnimationValues(bpy.data.objects[names[1]],type="float",prop="constraints['Follow Path'].offset_factor")
        camJsonObject["cam-path"] = functions.getPathPoints(cpath)
        camJsonObject["cam-stops"] = cam_stops
        camJsonObject["tgt-path"] = functions.getPathPoints(tpath)
        camJsonObject["tgt-stops"] = tgt_stops

    else:
        cam_pos = functions.getAnimationValues(objects[0],type="vector",prop="location")
        cam_tgt = functions.getAnimationValues(objects[1],type="vector",prop="location")
        camJsonObject["cam-positions"] = cam_pos
        camJsonObject["tgt-positions"] = cam_tgt

