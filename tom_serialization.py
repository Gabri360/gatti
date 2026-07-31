import json
from io import BytesIO
import tarfile
from camera import Camera
from image_network import ImageNetwork


def load():
    try:
        with tarfile.open("save.tom", "r:gz") as tar:
            cam = Camera.load(json.load(tar.extractfile("camera.json")))
            images = ImageNetwork.load(json.load(tar.extractfile("network.json")), cam)
    except FileNotFoundError:
        cam = Camera.empty()
        images = ImageNetwork.empty()
    return cam, images

def dump(cam, images):
    with tarfile.open("save.tom", "w:gz") as tar:
        # Camera
        data = BytesIO(json.dumps(cam.dump(), indent=4).encode("utf-8"))
        meta = tarfile.TarInfo("camera.json")
        meta.size = data.getbuffer().nbytes
        tar.addfile(meta, data)
        # Network
        data = BytesIO(json.dumps(images.dump(), indent=4).encode("utf-8"))
        meta = tarfile.TarInfo("network.json")
        meta.size = data.getbuffer().nbytes
        tar.addfile(meta, data)
