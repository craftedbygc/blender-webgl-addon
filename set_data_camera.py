import bpy
from mathutils import Quaternion
from . import functions


def create(jsonObject,coll):
    #------------ SPACER ---------------------
    # get camera settings 
    jsonObject["camera"] = {}
    job = jsonObject["camera"]

    #------------ SPACER ---------------------
    camFilm = None
    cam = None
    camDataMame = "CamData"
    for ob in coll.objects:
        name = ob.name
        if(name == "Camera"):
            cam = bpy.data.cameras[camDataMame]
            camFilm = bpy.data.cameras[camDataMame].sensor_width
    cam_stops,tgt_stops,camLens = functions.getAniAtt(cam)

    #------------ SPACER ---------------------
    cpath = functions.findObject("cam-path")
    tpath = functions.findObject("tgt-path")
    #------------ SPACER ---------------------

    job["focal-length"] = camLens
    job["film-gauge"] = camFilm
    job["cam-path"] = functions.getPathPoints(cpath)
    job["cam-stops"] = cam_stops
    job["tgt-path"] = functions.getPathPoints(tpath)
    job["tgt-stops"] = tgt_stops

    return {"FINISHED"}