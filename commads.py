import bpy 
import threading 

def open_command():  
    import subprocess
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

def stop_commad():
    import subprocess
    program = "cmd.exe "
    pause = "/K "
    run  = " Kill"
    command = program + pause + run
    cmd = subprocess.Popen(command) 



def run():
    t = threading.Thread(target=open_command)
    t.start()
    return {'FINISHED'}


def stop():
    t = threading.Thread(target=open_command)
    t.start()
    return {'FINISHED'}

