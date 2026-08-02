import json


with open("config/settings.json", "r") as file:
    settings = json.load(file)
    WIDTH = settings["width"]
    HEIGHT = settings["height"]
    ROOT = settings["root"]
