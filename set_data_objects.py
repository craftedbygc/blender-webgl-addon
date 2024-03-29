import bpy
from mathutils import Quaternion, Euler
from . import functions


def create(object):

            data = []

            #------------ SPACER ---------------------
            checkUserAni = bpy.context.scene.aniExport
            checkEulerRot = bpy.context.scene.eulerRot
            print(object.name)
            if object is not None:
                checkAni = functions.isTransformAni(object)
                if(checkAni and checkUserAni):
                    pos = functions.getAnimationValues(object,type="vector",prop="location")
                    sac = functions.getAnimationValues(object,type="vector",prop="scale")
                    rot = functions.getAnimationValues(object,type="vector",prop="rotation_euler")
    
                    
                    #------------ SPACER ---------------------
                    data.append(pos)
                    data.append(rot)
                    data.append(sac)
                    #------------ SPACER ---------------------
                    return data   
                    
                else: 
                    pos = object.location.copy()
                    sac = object.scale.copy()
                    if(checkEulerRot):
                        rot = object.rotation_euler
                        rot = [functions.rd(rot.x),functions.rd(rot.z),functions.rd(-rot.y)]
                    else:
                        rot = object.rotation_euler.to_quaternion()
                        rot.normalize()
                        rot = Quaternion((rot[0], rot[1], rot[3], -rot[2]))
                        rot = [functions.rd(rot[1]), functions.rd(rot[2]), functions.rd(rot[3]), functions.rd(rot[0])]

                    apos = [functions.rd(pos.x),functions.rd(pos.z),functions.rd(-pos.y)]
                    asac = [functions.rd(sac.x),functions.rd(sac.z),functions.rd(sac.y)]    

                    #------------ SPACER ---------------------

                    data.append(apos)
                    data.append(rot)
                    data.append(asac)
                    
                    #------------ SPACER ---------------------
                    return data       
            
            
                