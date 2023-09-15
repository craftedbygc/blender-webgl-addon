import bpy
from mathutils import Quaternion
from . import functions


def create(object):

            data = []

            #------------ SPACER ---------------------

            checkAni = functions.isTransformAni(object)
            
            if(checkAni):
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
            
            
                