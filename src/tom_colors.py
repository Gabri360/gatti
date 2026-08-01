import json


with open("config/palette.json", "r") as file:
    palette = json.load(file)
    BG_TRAVEL = palette["background-travel"]
    BG_MOVE = palette["background-move"]
    BG_SEARCH = palette["background-search"]
    TEXT = palette["text"]
