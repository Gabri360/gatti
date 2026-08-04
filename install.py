import json
from sys import argv
import os
from subprocess import call


if os.name not in {"posix", "nt"}:
    print("The current host isn't supported, can't install")
    exit()


elif os.name == "nt":
    common = os.path.join(os.environ["ProgramFiles"], "tom")

    if len(argv) == 1:
        # Install virtual environment
        os.mkdir(common)
        call(["python", "-m", "venv", os.path.join(common, "venv")])
        call([os.path.join(common, "venv", "Scripts", "python"), "-m", "pip", "install", "pygame-ce", "--quiet", "--quiet"])
        
        # Install assets
        call(["xcopy", "/i", "themes", os.path.join(common, "themes")])
        
        # Install source
        call(["xcopy", "/i", "src", os.path.join(common, "src")])
        with open(os.path.join(common, "src", "path"), "w") as file:
            file.write(os.path.join(common, "conf"))
        
        # Install config
        os.mkdir(os.path.join(common, "conf"))
        with open(os.path.join(common, "conf", "settings.json"), "w") as file:
            json.dump({
                "width": 1280,
                "height": 720,
                "theme": os.path.join(common, "themes", "default.json")
            }, file, indent=4)
        
        # Install 'executable'
        with open(os.path.join(common, "tom.bat"), "w") as file:
            file.write(' '.join(["call", os.path.join(common, "venv", "Scripts", "python"), os.path.join(common, "src", "main.py"), "%*"]))

            target = os.path.join(common, "tom.bat")
            shortcut = os.path.join(os.environ["USERPROFILE"], "Desktop", "tom.lnk")
            call(["powershell", f"$s=(New-Object -COM WScript.Shell).CreateShortcut('{shortcut}');$s.TargetPath='{target}';$s.Save()"])
    
elif os.name == "posix":
    common = "/usr/local"

    if len(argv) == 1:
    
        # Install virtual environment
        os.mkdir(os.path.join(common, "lib", "tom"))
        call(["python", "-m", "venv", os.path.join(common, "lib", "tom", "venv")])
        call([os.path.join(common, "lib", "tom", "venv", "bin", "python"), "-m", "pip", "install", "pygame-ce", "--quiet", "--quiet"])
        
        # Install assets
        os.mkdir(os.path.join(common, "share", "tom"))
        call(["cp", "-r", "themes", os.path.join(common, "share", "tom")])
        
        # Install source
        call(["cp", "-r", "src", os.path.join(common, "src", "tom")])
        with open(os.path.join(common, "src", "tom", "path"), "w") as file:
            file.write(os.path.join(common, "etc", "tom"))
    
        # Install config
        os.mkdir(os.path.join(common, "etc", "tom"))
        with open(os.path.join(common, "etc", "tom", "settings.json"), "w") as file:
            json.dump({
                "width": 1280,
                "height": 720,
                "theme": os.path.join(common, "share", "tom", "themes", "default.json")
            }, file, indent=4)
    
        # Install 'executable'
        with open(os.path.join(common, "bin", "tom"), "w") as file:
            python_exec = os.path.join(common, "lib", "tom", "venv", "bin", "python")
            tom_exec = os.path.join(common, "src", "tom", "main.py")
            file.write(f"{python_exec} -BO {tom_exec} $@\n")
        call(["chmod", "+x", os.path.join(common, "bin", "tom")])
    
    elif len(argv) == 2 and argv[1] == "uninstall":
        call(["rm", "-rf", os.path.join(common, "lib", "tom")])
        call(["rm", "-rf", os.path.join(common, "share", "tom")])
        call(["rm", "-rf", os.path.join(common, "src", "tom")])
        call(["rm", "-rf", os.path.join(common, "etc", "tom")])
        call(["rm", "-f", os.path.join(common, "bin", "tom")])
