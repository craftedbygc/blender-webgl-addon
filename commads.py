import bpy
from subprocess import Popen, PIPE
import atexit
#import pynput
#from pynput.keyboard import Key

# def run():  
#     program = "cmd.exe "
#     pause = "/K "
#     path = bpy.context.scene.saveFolderPath
#     pub = 'public' + 'baz "\\"'
#     clPath =  path.replace(pub, '')
#     path =  " cd "+ clPath
#     run  = " && npm start"
#     command = program + pause + path + run
#     print(command)
#     cmd = subprocess.Popen(command)

#     def stop():
#         print("========================= #") 
#         print("========================= #")
#         print("STOP NPM START")
#         subprocess.Popen('npm stop')
#         cmd.terminate()
#         print("========================= #")
#         print("========================= #") 
       
#     atexit.register(stop)


def run():
    #------------ SPACER ---------------------
    path = bpy.context.scene.saveFolderPath
    pub = 'public' + 'baz "\\"'
    clPath =  path.replace(pub, '')
    com1 =  " cd "+ clPath
    #------------ SPACER ---------------------
    com2 =  "npm run blender-start"
    com3 =  "npm run blender-stop"
    com4 =  "exit"
    #Create process
    process = Popen(com2, cwd=clPath, stdin=PIPE, stdout=PIPE, stderr=PIPE,shell=True)
 

    def stop():
        print("========================= #") 
        print("========================= #")
        print("STOP NPM START")
        Popen(com3, cwd=clPath, stdin=PIPE, stdout=PIPE, stderr=PIPE,shell=True)
        process.terminate()
        print("========================= #")
        print("========================= #") 
       
    atexit.register(stop)

