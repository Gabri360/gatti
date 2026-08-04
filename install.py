import json
from sys import argv
import os
from os.path import expanduser as homedir
from os import name as os_name
from os import listdir as ls
from subprocess import call


if os_name not in {"posix", "nt"}:
    print("The current host isn't supported, can't install")
    exit()


elif os_name == "nt":

    print("The windows host isn't currently supported, can't install")
    exit()

    if len(argv) == 1:
        # Install virtual environment
        call(["md", r"%ProgramFiles%\tom"])
        call(["python", "-m", "venv", r"%ProgramFiles%\tom"])
        call([r"%ProgramFiles%\tom\venv\Scripts\python", "-m", "pip", "install", "pygame-ce", "--quiet", "--quiet"])
        
        # Install assets
        call(["xcopy", "themes", r"%ProgramFiles%\tom\themes"])
        
        # Install source
        call(["xcopy", "src", r"%ProgramFiles%\tom\src"])
        
        # Install config
        with open(r"%ProgramFiles%\tom\settings.json", "w") as file:
            json.dump({
                "width": 1280,
                "height": 720,
                "theme": r"%ProgramFiles%\tom\themes\default.json"
            }, file, indent=4)
        
        # Install 'executable'
        with open(r"%ProgramFiles%\tom\tom.bat", "w") as file:
            file.write("@echo off\n")
            file.write(r"cmd /k \"cd /d %ProgramFiles%\tom\venv\Scripts & .\activate & cd /d %ProgramFiles%\tom & python -BO src\main.py\"")
            call(["powershell", r"\"$s=(New-Object -COM WScript.Shell).CreateShortcut('%USERPROFILE%\Desktop\tom.lnk');$s.TargetPath='%ProgramFiles%\tom\tom.bat';$s.Save()\""])
    
    elif len(argv) == 2 and argv[1] == "uninstall":
        call(["rmdir", "/s", "/q", r"%ProgramFiles%\tom"])

elif os_name == "posix":
    if len(argv) == 1:
    
        # Install virtual environment
        call(["mkdir", "/usr/local/lib/tom"])
        call(["python", "-m", "venv", "/usr/local/lib/tom/venv"])
        call(["/usr/local/lib/tom/venv/bin/python", "-m", "pip", "install", "pygame-ce", "--quiet", "--quiet"])
        
        # Install assets
        call(["mkdir", "/usr/local/share/tom"])
        call(["cp", "-r", "themes", "/usr/local/share/tom/"])
        
        # Install source
        call(["cp", "-r", "src", "/usr/local/src/tom"])
        with open("/usr/local/src/tom/path", "w") as file:
            file.write("/usr/local/etc/tom")
    
        # Install config
        call(["mkdir", "/usr/local/etc/tom/"])
        with open("/usr/local/etc/tom/settings.json", "w") as file:
            json.dump({
                "width": 1280,
                "height": 720,
                "theme": "/usr/local/share/tom/themes/default.json"
            }, file, indent=4)
    
        # Install 'executable'
        with open("/usr/local/bin/tom", "w") as file:
            file.write("/usr/local/lib/tom/venv/bin/python -BO /usr/local/src/tom/main.py $@\n")
        call(["chmod", "+x", "/usr/local/bin/tom"])
    
    elif len(argv) == 2 and argv[1] == "uninstall":
        call(["rm", "-rf", "/usr/local/lib/tom/"])
        call(["rm", "-rf", "/usr/local/share/tom/"])
        call(["rm", "-rf", "/usr/local/src/tom/"])
        call(["rm", "-rf", "/usr/local/etc/tom/"])
        call(["rm", "-f", "/usr/local/bin/tom"])
