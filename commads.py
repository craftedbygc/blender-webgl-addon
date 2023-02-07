import bpy 
import threading 

def open_command():  
    import subprocess
    program = "cmd.exe "
    pause = "/K "
    path =  " cd C:/laragon/www/blender-threejs-export-test/"
    run  = " && npm start"
    command = program + pause + path + run
    print(command)

    
    cmd = subprocess.Popen(command) 


def run():
    t = threading.Thread(target=open_command)
    t.start()
    return {'FINISHED'}
