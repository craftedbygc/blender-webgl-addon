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
            
            #------------ SPACER ---------------------
            f = open(filepath, "w")
            bpy.context.scene.frame_set(0)

            colNameTarget = "Scene"
            collArray = functions.getCollections(colNameTarget)
            for c in collArray:
                #Create main Scene object
                collName = c.name
                mainConv = functions.namingConvention(collName)
                jsonObject[mainConv] = {}

                #------------ SPACER ---------------------
                childColls = functions.getChildCollections(c)
                for cc in childColls:
                    childCollName = cc.name
                    childCov = functions.namingConvention(childCollName)
                    childCovTweak = childCov[2:]
                    jsonObject[mainConv][childCovTweak] = {}

                    #------------ SPACER ---------------------
                    # OBJECTS !!!!!!!!!
                    #Target the Objects collection to add data to json
                    if(childCovTweak == "objects"):
                        bpy.data.collections[childCollName].color_tag = 'COLOR_06'
                        oblist = [obj.name for obj in cc.all_objects]
                        oblist = sorted(oblist)
                        for name in oblist:
                            ob = cc.all_objects[name]
                            obname = functions.nameMatchScene(ob.name,collName)
                            obname = functions.namingConvention(obname)
                            data = set_data_objects.create(ob)
                            jsonObject[mainConv][childCovTweak][obname] = []
                            jsonObject[mainConv][childCovTweak][obname].append(data)

                    #------------ SPACER ---------------------
                    # INSTANCES MANUNAL !!!!!!!!!
                    #Target the Objects collection to add data to json
                    if(childCovTweak == "instances-manual"):
                        bpy.data.collections[childCollName].color_tag = 'COLOR_05'
                        for ccc in cc.children:
                            bpy.data.collections[cc.name].color_tag = 'COLOR_04'
                            oblist = [obj.name for obj in ccc.all_objects]
                            oblist = sorted(oblist)
                            inName = oblist[0]
                            conName = functions.namingConvention(inName)
                            jsonObject[mainConv][childCovTweak][conName] = []

                            for name in oblist:
                                ob = ccc.all_objects[name]
                                data = set_data_objects.create(ob)
                                jsonObject[mainConv][childCovTweak][conName].append(data)


                    #------------ SPACER ---------------------
                    # INSTANCES Nodes !!!!!!!!!
                    #Target the Objects collection to add data to json
                    if(childCovTweak == "instances-nodes"):
                        bpy.data.collections[childCollName].color_tag = 'COLOR_05'
                        for ccc in cc.children:
                            bpy.data.collections[cc.name].color_tag = 'COLOR_04'
                            if("Scattering-Bases"in cc.name):
                                oblist = [obj.name for obj in ccc.all_objects]
                                oblist = sorted(oblist)
                                for name in oblist:
                                    ob = ccc.all_objects[name]
                                    data,name = set_data_objects.create(ob) 
                                    obname = functions.nameMatchScene(name,collName)
                                    obname = functions.namingConvention(obname)                           
                                    jsonObject[mainConv][childCovTweak][obname] = []
                                    jsonObject[mainConv][childCovTweak][obname].append(data)


                    #------------ SPACER ---------------------
                    # CAMERA !!!!!!!!!
                    #Target the Camera to add data to json
                    if(childCovTweak == "camera"):
                        bpy.data.collections[childCollName].color_tag = 'COLOR_03'
                        for ccc in cc.children:
                            bpy.data.collections[ccc.name].color_tag = 'COLOR_02'
                        camJsonObject = jsonObject[mainConv][childCovTweak]
                        set_data_camera.create(camJsonObject,cc)

                    #------------ SPACER ---------------------
                    # PATHS !!!!!!!!!
                    #Target the paths to add data to json
                    if(childCovTweak == "paths"):
                        bpy.data.collections[childCollName].color_tag = 'COLOR_07'
                        oblist = [obj.name for obj in cc.all_objects]
                        oblist = sorted(oblist)
                        for name in oblist:
                            ob = cc.all_objects[name]
                            pathJsonObject = jsonObject[mainConv][childCovTweak]
                            set_data_obpaths.create(pathJsonObject,ob)
                            
                    
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