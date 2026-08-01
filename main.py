import json
import tarfile
import pygame as pg

from io import BytesIO
from sys import argv

from src import tom_params
from src import tom_program
from src import tom_serialization


if __name__ != "__main__":
    print("This python script shouldn't be imported")
    exit()


pg.init()
pg.display.set_caption("tom")
screen = pg.display.set_mode((tom_params.WIDTH, tom_params.HEIGHT))
prog = tom_program.TomProgram.empty()

try:
    # supply the last save as the one to be loaded
    if len(argv) == 1:
        try:
            with open(".save", "r") as file:
                path_save = file.read()
        except FileNotFoundError:
            print("No previous instance was found, please supply an argument")
            exit()

    # supply the save specified in the argument as the one to be loaded
    elif len(argv) == 2:
        path_save = argv[1]

    # to many arguments
    elif len(argv) > 2:
        print("To many arguments were supplied")
        exit()

    # loading supplied save
    with tarfile.open(path_save, "r:gz") as tar:
        data_cam = json.load(tar.extractfile("camera.json"))
        data_img = json.load(tar.extractfile("board.json"))
        tom_serialization.load_program(prog, data_cam, data_img)

except FileNotFoundError:
    # create a save using the supplied argument
    print(f"Couldn't find {path_save}, creating a new instance")


prog.run(tom_params.ROOT, screen)


# saving the latest program state
with tarfile.open(path_save, "w:gz") as tar:
    save = tom_serialization.dump_program(prog)
    # Camera
    data = BytesIO(json.dumps(save["camera"], indent=4).encode("utf-8"))
    meta = tarfile.TarInfo("camera.json")
    meta.size = data.getbuffer().nbytes
    tar.addfile(meta, data)
    # Network
    data = BytesIO(json.dumps(save["board"], indent=4).encode("utf-8"))
    meta = tarfile.TarInfo("board.json")
    meta.size = data.getbuffer().nbytes
    tar.addfile(meta, data)

# save last program instance identifier
with open(".save", "w") as file:
    file.write(path_save)


pg.quit()
exit()
