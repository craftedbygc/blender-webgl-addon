import bpy
from mathutils import Quaternion
from . import functions


def create(camJsonObject,coll):
    #------------ SPACER ---------------------
    camFilm = None
    cam = None
    camDataMame = "CamData"
    for ob in coll.objects:
        name = ob.name
        if("Camera" in name):
            cam = bpy.data.cameras[ob.name]
            camFilm = bpy.data.cameras[ob.name].sensor_width
    cam_stops,tgt_stops,camLens = functions.getAniAtt(cam)

    #------------ SPACER ---------------------
    cpath = functions.findObject("cam-path")
    tpath = functions.findObject("tgt-path")
    #------------ SPACER ---------------------

    camJsonObject["focal-length"] = camLens
    camJsonObject["film-gauge"] = camFilm
    camJsonObject["cam-path"] = functions.getPathPoints(cpath)
    camJsonObject["cam-stops"] = cam_stops
    camJsonObject["tgt-path"] = functions.getPathPoints(tpath)
    camJsonObject["tgt-stops"] = tgt_stops
    print("TBA-LEVEL-2")

    return {"FINISHED"}

def simple_create():
    print("working on it")
