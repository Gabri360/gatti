import json
from sys import argv
from os.path import expanduser as homedir
from os import name as os_name
from os import listdir as ls
from subprocess import call


if os_name == "nt":
    print("The installation is currently unavailable for windows")
    exit()

elif os_name != "posix":
    print("The current host isn't supported, can't install")
    exit()


if len(argv) == 1:

    # Install virtual environment
    call(["mkdir", "/usr/local/lib/tom"])
    call(["python", "-m", "venv", "/usr/local/lib/tom/venv"])
    call(["/usr/local/lib/tom/venv/bin/python", "-m", "pip", "install", "pygame-ce", "--quiet", "--quiet"])
    
    # Install assets
    call(["mkdir", "/usr/local/share/tom"])
    call(["cp", "-r", "themes", "/usr/local/share/tom/"])
    
    # Install source
    call(["mkdir", "/usr/local/src/tom"])
    for fname in ls("src"):
        call(["cp", f"src/{fname}", "/usr/local/src/tom/"])
    with open("/usr/local/src/tom/path", "w") as file:
        call(["echo", "-n", "/usr/local/etc/tom"], stdout=file)

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
        call(["echo", "-e", "/usr/local/lib/tom/venv/bin/python -BO /usr/local/src/tom/main.py $@"], stdout=file)
    call(["chmod", "+x", "/usr/local/bin/tom"])


elif len(argv) == 2 and argv[1] == "uninstall":
    call(["rm", "-rf", "/usr/local/lib/tom/"])
    call(["rm", "-rf", "/usr/local/share/tom/"])
    call(["rm", "-rf", "/usr/local/src/tom/"])
    call(["rm", "-rf", "/usr/local/etc/tom/"])
    call(["rm", "-f", "/usr/local/bin/tom"])
