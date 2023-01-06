import bpy
import os
import json
from . import functions
from . import set_data_objects
from . import set_data_camera
from . import set_data_obpaths

def exportData():
            #------------ SPACER -----------s----------
            file = "data.unseen"
            mainfolderpath = bpy.context.scene.saveFolderPath
            filepath = os.path.join(mainfolderpath, file)
            
           #------------ SPACER ---------------------
            jsonObject = {}
            jsonObject["instances"] = {}
            jsonObject["objects"] = {}
            jsonObject["paths"] = {}
            
            #------------ SPACER ---------------------
            f = open(filepath, "w")
            bpy.context.scene.frame_set(0)

            #------------ SPACER ---------------------

            collName = "Scene Instances"
            collmain = functions.findCollection(collName)
            bpy.data.collections[collName].color_tag = 'COLOR_05'
            
            for coll in collmain.children:
                    bpy.data.collections[coll.name].color_tag = 'COLOR_04'
                    cName = coll.name
                    myList = [obj.name for obj in coll.all_objects]
                    myList = sorted(myList)
                    inName = myList[0]
                    conName = functions.namingConvention(inName)
                    jsonObject["instances"][conName] = []
                    
                    for name in myList:
                        ob = coll.all_objects[name] 
                        set_data_objects.create(jsonObject,ob,inName,False)


            #------------ SPACER ---------------------
            collName = "Scene Objects"
            collmain = functions.findCollection(collName)
            bpy.data.collections[collName].color_tag = 'COLOR_06'
            
            oblist = [obj.name for obj in collmain.all_objects]
            oblist = sorted(oblist)
                  
            for name in oblist:
                ob = collmain.all_objects[name]
                set_data_objects.create(jsonObject,ob,ob.name,True)
            
            #------------ SPACER ---------------------
            collName = "Scene Camera"
            collmain = functions.findCollection(collName)
            bpy.data.collections[collName].color_tag = 'COLOR_03'
            for coll in collmain.children:
                bpy.data.collections[coll.name].color_tag = 'COLOR_02'
            set_data_camera.create(jsonObject,collmain)

            #------------ SPACER ---------------------

            collName = "Scene Objects Paths"
            collmain = functions.findCollection(collName)
            bpy.data.collections[collName].color_tag = 'COLOR_07'
            
            oblist = [obj.name for obj in collmain.all_objects]
            oblist = sorted(oblist)

            for name in oblist:
                ob = collmain.all_objects[name]
                set_data_obpaths.create(jsonObject,ob)

            #------------ SPACER ---------------------
                    
            if(bpy.context.scene.minify):
                indentVal = None
            else:
                indentVal = 1
                
            objects = json.dumps(jsonObject, indent=indentVal, ensure_ascii=True,separators=(',', ':'))
            f.write(objects)
            f.close()


            #open and read the file after the appending:
            f = open(filepath, "r")
            #print(f.read())
            bpy.context.scene.frame_set(1)
            return