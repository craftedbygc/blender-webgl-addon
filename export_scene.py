import bpy
import os
import json
from . import functions
from . import export_import
from . import export_materials
from . import set_data_objects
from . import set_data_camera
from . import set_data_obpaths
from . import set_data_geoinstances

def main_scene_export(draco,fullScene):

    #------------ SPACER ---------------------
    # Fetch High level collection and create the Name for the unseen file
    cNameTarget = "Scene"
    c = functions.findCollectionWithString(cNameTarget)
    dataName = c.name.replace(cNameTarget, "")
    dataName = dataName.replace(" ", "")
    dataName = functions.namingConvention(dataName)
    dataName = dataName + ".unseen"

    #------------ SPACER ---------------------
    # Initial Setup and Variables
    mainfolderpath = bpy.context.scene.saveFolderPath
    childColls = functions.getChildCollections(c)
    format = 'GLB'
    obcount = 0
    file_size_mb = 0.0
    total_textures = 0
    bpy.context.scene.fileSize = file_size_mb
    bpy.context.scene.frame_set(0)
    currentSelectedOb = bpy.context.active_object
    bpy.context.scene.exportState = True

    #------------ SPACER ---------------------
    # Open Json File and check if it exists
    filepath = os.path.join(mainfolderpath, dataName)
    global jsonObject
    try:
        with open(filepath, "r") as json_file:
            # Load the JSON content
            jsonObject = json.load(json_file)
            f = open(filepath, "w")

            if bpy.context.scene.camPaths == False:
                target_objects = [{"key": "cam-path"}, {"key": "tgt-path"}]
                for target in target_objects:
                    if target in jsonObject:
                        jsonObject.remove(target)
            else:
                target_objects = [{"key": "cam-positions"}, {"key": "tgt-positions"}]
                for target in target_objects:
                    if target in jsonObject:
                        jsonObject.remove(target)


    except:
        f = open(filepath, "w")
        jsonObject = {}
   

    #------------ SPACER ---------------------
    # Print into console so we can mark the start of the export
    print("========================= #") 
    print("========================= #")
    print("BATCH START") 
    print("========================= #")
    print("========================= #") 


    #------------ SPACER ---------------------
    # Transverse the scene and go over each collection
    if len(childColls) > 0:
        for cc in childColls:
            childCollName = cc.name
            childCov = functions.namingConvention(childCollName)
            childCovTweak = childCov 
            
            #------------ SPACER ---------------------
            #Check if the current sellect collection is usable and create an object from it
            collist = ("objects","camera","paths","empties","instances-manual","instances-nodes")
            if childCovTweak in collist:
                if childCovTweak not in jsonObject:
                    if "instances" in childCovTweak:
                        if "instances" not in jsonObject:
                            jsonObject["instances"] = {}
                    else:
                        jsonObject[childCovTweak] = {}
            
            #------------ SPACER ---------------------
            # CAMERA !!!!!!!!!
            #Target the Camera to add data to json
            if(childCovTweak == "camera"):
                bpy.data.collections[childCollName].color_tag = 'COLOR_03'
                for ccc in cc.children:
                    bpy.data.collections[ccc.name].color_tag = 'COLOR_02'
                camJsonObject = jsonObject[childCovTweak]
                # set_data_camera.create(camJsonObject,cc)


            #------------ SPACER ---------------------
            # PATHS !!!!!!!!!
            #Target the paths to add data to json
            if(childCovTweak == "paths"):
                bpy.data.collections[childCollName].color_tag = 'COLOR_07'
                if len(cc.all_objects) > 0:
                    oblist = [obj.name for obj in cc.all_objects]
                    oblist = sorted(oblist)
                    for name in oblist:
                        ob = cc.all_objects[name]
                        pathJsonObject = jsonObject[childCovTweak]
                        set_data_obpaths.create(pathJsonObject,ob)
                else:
                    print("NO PATHS TO ADD TO DATA JSON")
            
            #------------ SPACER ---------------------
            # INTERFACE !!!!!!!!!
            #Target the Objects collection to add data to json
            if(childCovTweak == "empties"):
                bpy.data.collections[childCollName].color_tag = 'COLOR_05'
                for ccc in cc.children:
                    if len(ccc.all_objects) > 0:
                        bpy.data.collections[ccc.name].color_tag = 'COLOR_04'
                        oblist = [obj.name for obj in ccc.all_objects]
                        oblist = sorted(oblist)
                        inName = oblist[0]
                        conName = functions.namingConvention(inName)

                        for name in oblist:
                            ob = ccc.all_objects[name]
                            data = set_data_objects.create(ob)
                            jsonObject[childCovTweak][conName] = data

                    else:
                        print("NO EMPTIES TO ADD TO DATA JSON")             
                    
            #------------ NEW COLL TYPE ---------------------  
            #------------ NEW COLL TYPE ---------------------
            #------------ NEW COLL TYPE ---------------------
            #------------ NEW COLL TYPE ---------------------
            # Do export action to the current select collection
            if(childCovTweak == "objects" or childCovTweak == "rigged-objects"):
                bpy.data.collections[childCollName].color_tag = 'COLOR_06'
                if len(cc.all_objects) > 0:
                    oblist = [obj.name for obj in cc.all_objects]
                    oblist = sorted(oblist)
                    for name in oblist:
                        ob = cc.all_objects[name]
                        obname = functions.namingConvention(ob.name)
                        
                        #------------ SPACER ---------------------
                        # Check if object changed
                        bpy.context.view_layer.update()
                        try:
                            prop = functions.getproperty(ob,"updated")
                        except:
                            functions.createProp(ob,"updated",0)

                        if fullScene:
                            prop = 2

                        #------------ SPACER ---------------------
                        # Check if rigged
                        obp = ob
                        if "rigged-" in childCovTweak:
                            obp = ob.parent
                            childCovTweak = childCovTweak.replace("rigged-", "") 

                        #------------ SPACER ---------------------
                        # Export the selected object
                            
                        if prop>0:
                            obcount, file_size_mb = export_import.glbExpOp(mainfolderpath,format,ob,draco,obcount,skinned=False)

                            #Export the image and return the texture objects
                            textures =  None
                            matSettings = None

                            if prop>1:
                                textures, matSettings = export_materials.export(mainfolderpath,ob)
                                total_textures += len(textures)
                        
                            #WRITTE THE ob to json
                            data = set_data_objects.create(obp)

                            #------------ SPACER ---------------------
                            #Add settings to objects
                            settings = {}
                            if textures !=None and matSettings !=None:
                                settings["material"] = matSettings
                                settings["textures"] = textures

                            #------------ SPACER ---------------------
                            #Add object info to main object
                            data.append(settings)
                            jsonObject[childCovTweak][obname] = data

                            
                            #------------ SPACER ---------------------
                            #Reset Updater and print
                            ob["updated"] = 0
                            print(ob.name,">>> EXPORTED !!!!")
                        else:
                            print(ob.name,">>> NOT CHANGED")
                        #Add the objects for extra information
                        bpy.context.scene.totalTex = total_textures
                        bpy.context.scene.fileSize += file_size_mb
                        bpy.context.scene.obCount = obcount

                else:
                    print("NO OBJECTS TO ADD TO DATA JSON")

            # --------- INSTANCES MANUAL ---------- 
            if(childCovTweak == "instances-manual"):
                bpy.data.collections[childCollName].color_tag = 'COLOR_06'

                for instanceCol in cc.children: 
                    # Go through all instances in that collection
                    if len(instanceCol.all_objects) > 0:

                        # Get all the instanced objects in the collection
                        oblist = [obj.name for obj in instanceCol.all_objects]
                        oblist = sorted(oblist)
                        count = 0
                        toUpdate = False

                        for name in oblist:
                            ob = instanceCol.all_objects[name] # Get the instanced object
                            obname = functions.namingConvention(ob.name)

                            #JSON data structure for instances 'instance name'; [ [positions], {material, textures} ]
                            if (count == 0):
                                jsonName = obname
                                # Create empty data
                                data = [] # Create master data
                                transforms = [] # Create transforms data (position, scale, rotation)
                                settings = {} # Create empty settings object for material and textures

                                #------------ SPACER ---------------------
                                # Check if object changed
                                bpy.context.view_layer.update()
                                try:
                                    prop = functions.getproperty(ob,"updated")
                                except:
                                    functions.createProp(ob,"updated",0)
                                
                                if prop>0:
                                    toUpdate = True
                                    # Export the first model if it has changes
                                    obcount = export_import.glbExpOp(mainfolderpath,format,ob,draco,obcount,skinned=False)

                                    #Export the image and return the texture objects
                                    textures, matSettings = export_materials.export(mainfolderpath,ob)

                                    #------------ SPACER ---------------------
                                    #Add settings to objects
                                    if textures !=None and matSettings !=None:
                                        settings["material"] = matSettings
                                        settings["textures"] = textures
                                    
                                    #------------ SPACER ---------------------
                                    #Reset Updater and print
                                    ob["updated"] = 0
                                    print(ob.name,">>> EXPORTED !!!!")
                                else:
                                    print(ob.name,">>> NOT CHANGED")
                        
                            transforms.append(set_data_objects.create(ob)) # Append the transfroms data
                            count += 1 # Iterate

                        # Add to JSON object
                        if (toUpdate == True):
                            # Check if object has been updated -> overwrite everything
                            data.append(transforms)
                            data.append(settings)
                            jsonObject["instances"][jsonName] = data
                        else:
                            # Change only transforms data
                            if jsonName in jsonObject["instances"]:
                                # Data is present -> override
                                jsonObject["instances"][jsonName][0] = transforms
                            else:
                                # No previous data -> append
                                # Occurs also when you keep the blend file open and no changes are detected, but we don't have existing data -> create data without settings
                                jsonObject["instances"][jsonName] = []
                                jsonObject["instances"][jsonName].append(transforms)
                    else: 
                        print(f'No instances in {instanceCol.name}')
            
            # ----------- INSTANCES NODES ------------- 
            if(childCovTweak == "instances-nodes"):
                # Create temp json object to prevent override of variables
                tempJson = {}

                bpy.data.collections[childCollName].color_tag = 'COLOR_06'
                
                # Get the Instanced Geometry to export the GLBs
                instancedGeoCol = functions.getNamedChildCollections("Instanced Geometry", cc)[0]
                bpy.data.collections[instancedGeoCol.name].color_tag = 'COLOR_04'

                # Get all models
                oblist = [obj.name for obj in instancedGeoCol.all_objects]
                oblist = sorted(oblist)

                for name in oblist:
                    ob = instancedGeoCol.all_objects[name]
                    obname = functions.namingConvention(ob.name)

                    # Create temp data   
                    tempJson[obname] = {}  
                    tempJson[obname]["transforms"] = []
                    tempJson[obname]["settings"] = {}
                    tempJson[obname]["toUpdate"] = False

                    #------------ SPACER ---------------------
                    # Check if object changed
                    bpy.context.view_layer.update()
                    try:
                        prop = functions.getproperty(ob,"updated")
                    except:
                        functions.createProp(ob,"updated",0)

                    #------------ SPACER ---------------------
                    # Export the instanced object and get material data
                    if prop>0:
                        tempJson[obname]["toUpdate"] = True # Set to True to check later
                        obcount = export_import.glbExpOp(mainfolderpath,format,ob,draco,obcount,skinned=False)

                        #Export the image and return the texture objects
                        textures, matSettings = export_materials.export(mainfolderpath,ob)

                        #------------ SPACER ---------------------
                        #Add settings to objects
                        if textures !=None and matSettings !=None:
                            tempJson[obname]["settings"]["material"] = matSettings
                            tempJson[obname]["settings"]["textures"] = textures

                        #------------ SPACER ---------------------
                        #Reset Updater and print
                        ob["updated"] = 0
                        print(ob.name,">>> EXPORTED !!!!")
                    else:
                        print(ob.name,">>> NOT CHANGED")

                # Get the scattering bases collection to grab the data
                scatteringBasesCol = functions.getNamedChildCollections("Scattering Bases", cc)[0]
                bpy.data.collections[scatteringBasesCol.name].color_tag = 'COLOR_04'

                # Get all bases
                oblist = [obj.name for obj in scatteringBasesCol.all_objects]
                oblist = sorted(oblist)

                if(len(oblist) > 0):
                    depsgraph = bpy.context.evaluated_depsgraph_get() # Create evaluated graph for the whole scene
                else:
                    print("NO NODE INSTANCES TO ADD TO DATA JSON")
                
                for name in oblist:
                    # Go through all bases
                    ob = scatteringBasesCol.all_objects[name]
                    obname = functions.namingConvention(ob.name)

                    # Get the object in the evaluated dependency graph to attach instances
                    evalOb = ob.evaluated_get(depsgraph)
                    set_data_geoinstances.find(depsgraph, evalOb, tempJson)

                # Finally, iterate through the temp object, copying correct values to the actual json
                for instanceName, instanceData in tempJson.items():
                    if (instanceData['toUpdate'] == True):
                            # Check if object has been updated -> overwrite everything
                            data = []
                            data.append(instanceData['transforms'])
                            data.append(instanceData['settings'])
                            jsonObject["instances"][instanceName] = data
                    else:
                        # Change only transforms data
                        if instanceName in jsonObject["instances"]:
                            # Data is present -> override
                            jsonObject["instances"][instanceName][0] = instanceData['transforms']
                        else:
                            # No previous data -> append
                            # Occurs also when you keep the blend file open and no changes are detected, but we don't have existing data -> create data without settings
                            jsonObject["instances"][instanceName] = []
                            jsonObject["instances"][instanceName].append(instanceData['transforms'])
    else:
        print("NO COLLECTIONS IN SCENE")


    #------------ SPACER ---------------------  
    #------------ SPACER ---------------------
    #------------ SPACER ---------------------
    #------------ SPACER ---------------------  
    # Writte to Json file an apply final changes
    
    if(bpy.context.scene.minify):
        indentVal = None
    else:
        indentVal = 1
    
    objects = json.dumps(jsonObject, indent=indentVal, ensure_ascii=True,separators=(',', ':'))
    f.write(objects)
    f.close()
    bpy.context.scene.frame_set(1)
    bpy.context.scene.exportState = False
    functions.forceselect(currentSelectedOb)

    #------------ SPACER ---------------------
    print("========================= #") 
    print("========================= #")
    print("EXPORT DONE") 
    print("- Total Objects Exported:",obcount)
    print("========================= #")
    print("========================= #") 

    return