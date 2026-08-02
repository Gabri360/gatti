import json
import tom_params as tp


with open(tp.THEME, "r") as file:
    palette = json.load(file)
    BG_TRAVEL = palette["background-travel"]
    BG_MOVE = palette["background-move"]
    BG_SEARCH = palette["background-search"]
    TEXT = palette["text"]
