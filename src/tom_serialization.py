import pygame as pg
import tom_math as tm


def load_program(prog, data_cam, data_img):

    # loading camera data
    prog.board.cam_pos = tm.Vec2(data_cam["position"]["x"], data_cam["position"]["y"])
    prog.board.cam_scale = data_cam["scale"]

    # loading image data
    for img in data_img:
        prog.board.add(
            path=img["path"],
            srf=pg.image.load(img["path"]).convert_alpha(),
            pos=tm.Vec2(img["position"]["x"], img["position"]["y"]),
            scale=img["scale"]
        )


def dump_program(prog):
    return {
        "camera": {
            "position": {
                "x": prog.board.cam_pos.x,
                "y": prog.board.cam_pos.y
            },
            "scale": prog.board.cam_scale
        },
        "board": [{
            "path": prog.board.img_path[i],
            "position": {
                "x": prog.board.img_pos[i].x,
                "y": prog.board.img_pos[i].y
            },
            "scale": prog.board.img_scale[i]
        } for i in range(prog.board.img_count)]
    }
