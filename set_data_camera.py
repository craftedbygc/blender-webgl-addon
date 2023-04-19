import bpy
from mathutils import Quaternion
from . import functions


def oldcreate(camJsonObject,coll):
    #------------ SPACER ---------------------
    camFilm = None
    cam = None
    camDataMame = "CamData"
    for ob in coll.objects:
        name = ob.name
        if("Camera" in name):
            cam = bpy.data.cameras[ob.name]
            camFilm = bpy.data.cameras[ob.name].sensor_width
    
    target = functions.findObject("cam_pos")
    print("TBA-CHECK-1",functions.getAnimationValues(target,type="vector",prop="location"))
   
    # cam_stops,tgt_stops,camLens = getAniAtt(cam,proprety="location")

    # #------------ SPACER ---------------------
    # cpath = functions.findObject("cam-path")
    # tpath = functions.findObject("tgt-path")
    # #------------ SPACER ---------------------

    # camJsonObject["focal-length"] = camLens
    # camJsonObject["film-gauge"] = camFilm
    # camJsonObject["cam-path"] = functions.getPathPoints(cpath)
    # camJsonObject["cam-stops"] = cam_stops
    # camJsonObject["tgt-path"] = functions.getPathPoints(tpath)
    # camJsonObject["tgt-stops"] = tgt_stops
    # print("TBA-LEVEL-2")

    # return {"FINISHED"}

def create(camJsonObject,coll):

    #Objects needed
    names = ("cam_pos","cam_tgt","Camera")
    objects = functions.findObjects(names)

    cam_pos = functions.getAnimationValues(objects[0],type="vector",prop="location")
    cam_tgt = functions.getAnimationValues(objects[1],type="vector",prop="location")
    camLens = functions.getAnimationValues(objects[2],type="float",prop="data.lens")
    print(cam_pos,cam_tgt,camLens)





#------------ SPACER ---------------------
def oldgetAni(cam):
    sce = bpy.data.scenes["Scene"]
    frame_start = sce.frame_start
    frame_end = sce.frame_end
    #------------ SPACER ---------------------
    camLens = []
    cam_stops = []
    tgt_stops = []
    prevLens = -1
    prevCam = -1
    prevTgt = -1
    #------------ SPACER ---------------------
    for f in range(frame_start, frame_end+1):
        sce.frame_set(f)

        getCamStop = bpy.data.objects["cam_pos"].constraints["Follow Path"].offset_factor
        getTgtStop = bpy.data.objects["cam_tgt"].constraints["Follow Path"].offset_factor
        getLens = cam.lens
        #------------ SPACER ---------------------
        if(prevLens == getLens):
            camLens.append(getLens)
            
        if(prevCam == getCamStop):
            cam_stops.append(crd(getCamStop,5))

        if(prevTgt == getTgtStop):
            tgt_stops.append(crd(getTgtStop,5))
        #------------ SPACER ---------------------
        prevLens = getLens
        prevCam = getCamStop
        prevTgt = getTgtStop

        
    cam_stops = getunic(cam_stops)
    tgt_stops = getunic(tgt_stops)
    camLens = getunic(camLens)  
    
    return cam_stops, tgt_stops, camLens

