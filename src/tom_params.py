import json

cwd = '/'.join(__file__.split('/')[:-1])
with open(f"{cwd}/path", "r") as file:
    path = '/'.join([line for line in file] + ["settings.json"])

with open(path, "r") as file:
    settings = json.load(file)
    WIDTH = settings["width"]
    HEIGHT = settings["height"]
    THEME = settings["theme"]
