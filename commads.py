import bpy
import subprocess
import atexit

def run():  
    program = "cmd.exe "
    pause = "/K "
    path = bpy.context.scene.saveFolderPath
    pub = 'public' + 'baz "\\"'
    clPath =  path.replace(pub, '')
    path =  " cd "+ clPath
    run  = " && npm start"
    command = program + pause + path + run
    print(command)
    cmd = subprocess.Popen(command)

    def stop():
        print("========================= #") 
        print("========================= #")
        print("STOP NPM START")
        cmd.terminate()
        print("========================= #")
        print("========================= #") 
       
    atexit.register(stop)


