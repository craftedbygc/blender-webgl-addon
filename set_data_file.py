import bpy
import os
import json
from . import functions
from . import set_data_objects
from . import set_data_camera
from . import set_data_obpaths
from . import set_data_geoinstances

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

                        # Select Instancing geo and Scattering base collections separately - TO DO
                        # bpy.data.collections[childCollName].color_tag = 'COLOR_05'
                        # instancedGeoCol = functions.getCollections("Instanced-Geometry")[0]
                        # bpy.data.collections[instancedGeoCol.name].color_tag = 'COLOR_04'
                        # # instancedGeoColName = instancedGeoCol.name[2:]
                        # oblist = [obj.name for obj in instancedGeoCol.all_objects]
                        # oblist = sorted(oblist)
                        # print(oblist)
                        # for name in oblist:
                        #     ob = instancedGeoCol.all_objects[name]
                        #     # obname = functions.nameMatchScene(name,collName)
                        #     obname = functions.namingConvention(name)                           
                        #     jsonObject[mainConv][childCovTweak][obname] = [] # Create an empty array for each geometry that is instanced
                        #     print(f'create temp instance json {jsonObject[mainConv][childCovTweak]}')

                        # scatteringBasesCol = functions.getCollections("Scattering-Bases")[0]
                        # bpy.data.collections[scatteringBasesCol.name].color_tag = 'COLOR_04'
                        # oblist = [obj.name for obj in scatteringBasesCol.all_objects]
                        # oblist = sorted(oblist)
                        # print(oblist)
                        # depsgraph = bpy.context.evaluated_depsgraph_get() # Create evaluated graph for the whole scene
                        # for name in oblist:
                        #     # Go through all bases
                        #     ob = scatteringBasesCol.all_objects[name]
                        #     # Get the object in the evaluated dependency graph to attach instances
                        #     evalOb = ob.evaluated_get(depsgraph)
                        #     set_data_geoinstances.find(depsgraph, evalOb, jsonObject[mainConv][childCovTweak], collName)

                        for ccc in cc.children:
                            # Go through the Scattering-Bases & Instanced-Geometry collections - important that Instanced-Geometry is first in the list !! (for now)
                            bpy.data.collections[ccc.name].color_tag = 'COLOR_04'
                            subCollectionName = ccc.name
                            subCollectionName = subCollectionName[2:]
                            if("Instanced-Geometry"in subCollectionName):
                                oblist = [obj.name for obj in ccc.all_objects]
                                oblist = sorted(oblist)
                                for name in oblist:
                                    ob = ccc.all_objects[name]
                                    obname = functions.nameMatchScene(name,collName)
                                    obname = functions.namingConvention(obname)                           
                                    jsonObject[mainConv][childCovTweak][obname] = [] # Create an empty array for each geometry that is instanced
                                    # print(f'create temp instance json {jsonObject[mainConv][childCovTweak]}')
                            if ("Scattering-Bases" in subCollectionName):
                                # Get all base objects
                                oblist = [obj.name for obj in ccc.all_objects]
                                oblist = sorted(oblist)
                                depsgraph = bpy.context.evaluated_depsgraph_get() # Create evaluated graph for the whole scene
                                for name in oblist:
                                    # Go through all bases
                                    ob = ccc.all_objects[name]
                                    # Get the object in the evaluated dependency graph to attach instances
                                    evalOb = ob.evaluated_get(depsgraph)
                                    set_data_geoinstances.find(depsgraph, evalOb, jsonObject[mainConv][childCovTweak], collName)


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