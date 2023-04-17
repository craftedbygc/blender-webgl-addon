import bpy
import os
import json
from . import functions
from . import export_batch
from . import export_materials
from . import set_data_objects
from . import set_data_camera
from . import set_data_obpaths
from . import set_data_geoinstances

def main_scene_export(draco):

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
                set_data_camera.create(camJsonObject,cc)

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

                        #------------ SPACER ---------------------
                        # Check if rigged
                        obp = ob
                        if "rigged-" in childCovTweak:
                            obp = ob.parent
                            childCovTweak = childCovTweak.replace("rigged-", "") 

                        #------------ SPACER ---------------------
                        # Export the selected object
                            
                        if prop>0:
                            obcount = export_batch.glbExpOp(mainfolderpath,format,ob,draco,obcount,skinned=False)

                            #Export the image and return the texture objects
                            textures, matSettings = export_materials.export(mainfolderpath,ob)
                        
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

                else:
                    print("NO OBJECTS TO ADD TO DATA JSON")
            

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