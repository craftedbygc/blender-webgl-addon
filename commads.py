import bpy
from subprocess import Popen, PIPE
import atexit

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
    com2 =  "npm start"
    com3 =  "npm stop"
    print(com1)
    process = Popen(com2, cwd=clPath, shell=True)

    def stop():
        print("========================= #") 
        print("========================= #")
        print("STOP NPM START")
        process = Popen(com3,cwd=clPath,shell=True)
        process.terminate()
        print("========================= #")
        print("========================= #") 
       
    atexit.register(stop)

