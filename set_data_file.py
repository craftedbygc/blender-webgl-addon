import bpy
import os
import json
from . import functions
from . import set_data_objects
from . import set_data_camera
from . import set_data_obpaths
from . import set_data_geoinstances

def exportData():

            cNameTarget = "Scene"
            c = functions.findCollectionWithString(cNameTarget)
            dataName = c.name.replace(cNameTarget, "")
            dataName = dataName.replace(" ", "")
            dataName = functions.namingConvention(dataName)
            dataName = dataName + ".unseen"

            #------------ SPACER -----------s----------
            #file = "data.unseen"
            
            mainfolderpath = bpy.context.scene.saveFolderPath
            filepath = os.path.join(mainfolderpath, dataName)
            
           #------------ SPACER ---------------------
            jsonObject = {}
            
            #------------ SPACER ---------------------
            f = open(filepath, "w")
            bpy.context.scene.frame_set(0)

            jsonObject = {}

            #------------ SPACER ---------------------
            childColls = functions.getChildCollections(c)
            for cc in childColls:
                childCollName = cc.name
                childCov = functions.namingConvention(childCollName)
                childCovTweak = childCov
                if(childCovTweak == "objects"):
                    jsonObject[childCovTweak] = {}
                if(childCovTweak == "camera"):
                    jsonObject[childCovTweak] = {}
                if(childCovTweak == "paths"):
                    jsonObject[childCovTweak] = {}
                if(childCovTweak == "empties"):
                    jsonObject[childCovTweak] = {}
                if(childCovTweak == "instances-manual" or childCovTweak == "instances-nodes"):
                    jsonObject["instances"] = {}

            for cc in childColls:
                childCollName = cc.name
                childCov = functions.namingConvention(childCollName)
                childCovTweak = childCov
               

                #------------ SPACER ---------------------
                # OBJECTS !!!!!!!!!
                #Target the Objects collection to add data to json
                if(childCovTweak == "objects"):
                    bpy.data.collections[childCollName].color_tag = 'COLOR_06'
                    oblist = [obj.name for obj in cc.all_objects]
                    oblist = sorted(oblist)
                    for name in oblist:
                        ob = cc.all_objects[name]
                        obname = functions.namingConvention(ob.name)
                        data = set_data_objects.create(ob)
                        jsonObject[childCovTweak][obname] = []
                        jsonObject[childCovTweak][obname].append(data)

                #------------ SPACER ---------------------
                # RIGGED OBJECTS !!!!!!!!!
                #Target the Objects collection to add data to json
                if(childCovTweak == "rigged-objects"):
                    bpy.data.collections[childCollName].color_tag = 'COLOR_06'
                    oblist = [obj.name for obj in cc.all_objects]
                    oblist = sorted(oblist)
                    for name in oblist:
                        ob = cc.all_objects[name]
                        if(ob.type == 'MESH'):
                            obname = functions.namingConvention(ob.name)
                            obp = ob.parent
                            data = set_data_objects.create(obp)
                            childCovTweak = childCovTweak.replace("rigged-", "")       
                            jsonObject[childCovTweak][obname] = []
                            jsonObject[childCovTweak][obname].append(data)
                
                #------------ SPACER ---------------------
                # CAMERA !!!!!!!!!
                #Target the Camera to add data to json
                if(childCovTweak == "camera"):
                    bpy.data.collections[childCollName].color_tag = 'COLOR_03'
                    for ccc in cc.children:
                        bpy.data.collections[ccc.name].color_tag = 'COLOR_02'
                    camJsonObject = jsonObject[childCovTweak]
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
                        pathJsonObject = jsonObject[childCovTweak]
                        set_data_obpaths.create(pathJsonObject,ob)

                 #------------ SPACER ---------------------
                # INTERFACE !!!!!!!!!
                #Target the Objects collection to add data to json
                if(childCovTweak == "empties"):
                    bpy.data.collections[childCollName].color_tag = 'COLOR_05'
                    for ccc in cc.children:
                        bpy.data.collections[ccc.name].color_tag = 'COLOR_04'
                        oblist = [obj.name for obj in ccc.all_objects]
                        oblist = sorted(oblist)
                        inName = oblist[0]
                        conName = functions.namingConvention(inName)
                        jsonObject[childCovTweak][conName] = []
                        for name in oblist:
                            ob = ccc.all_objects[name]
                            data = set_data_objects.create(ob)
                            jsonObject[childCovTweak][conName].append(data)       
       

                #------------ SPACER ---------------------
                # INSTANCES MANUNAL !!!!!!!!!
                #Target the Objects collection to add data to json
                if(childCovTweak == "instances-manual"):
                    childCovTweak = childCovTweak[:-7]
                    bpy.data.collections[childCollName].color_tag = 'COLOR_05'
                    for ccc in cc.children:
                        bpy.data.collections[ccc.name].color_tag = 'COLOR_04'
                        oblist = [obj.name for obj in ccc.all_objects]
                        oblist = sorted(oblist)
                        inName = oblist[0]
                        conName = functions.namingConvention(inName)
                        jsonObject[childCovTweak][conName] = []

                        for name in oblist:
                            ob = ccc.all_objects[name]
                            data = set_data_objects.create(ob)
                            jsonObject[childCovTweak][conName].append(data)


                #------------ SPACER ---------------------
                # INSTANCES Nodes !!!!!!!!!
                #Target the Instances-Nodes collection to add data to json
                if(childCovTweak == "instances-nodes"):
                    childCovTweak = childCovTweak[:-6]
                    # Select Instancing geo and Scattering base collections separately
                    bpy.data.collections[childCollName].color_tag = 'COLOR_05'
                    instancedGeoCol = functions.getNamedChildCollections("Instanced Geometry", cc)[0]
                    bpy.data.collections[instancedGeoCol.name].color_tag = 'COLOR_04'
                    oblist = [obj.name for obj in instancedGeoCol.all_objects]
                    oblist = sorted(oblist)
                    for name in oblist:
                        ob = instancedGeoCol.all_objects[name]
                        obname = functions.namingConvention(name)                           
                        jsonObject[childCovTweak][obname] = [] # Create an empty array for each geometry that is instanced
                        # print(f'create temp instance json {jsonObject[childCovTweak]}')

                    scatteringBasesCol = functions.getNamedChildCollections("Scattering Bases", cc)[0]
                    bpy.data.collections[scatteringBasesCol.name].color_tag = 'COLOR_04'
                    oblist = [obj.name for obj in scatteringBasesCol.all_objects]
                    oblist = sorted(oblist)
                    if(len(oblist) > 0):
                        depsgraph = bpy.context.evaluated_depsgraph_get() # Create evaluated graph for the whole scene
                    else:
                        print("No geo instancing bases!")
                    for name in oblist:
                        # Go through all bases
                        ob = scatteringBasesCol.all_objects[name]
                        # Get the object in the evaluated dependency graph to attach instances
                        evalOb = ob.evaluated_get(depsgraph)
                        set_data_geoinstances.find(depsgraph, evalOb, jsonObject[childCovTweak])
                    
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