import pygame as pg
from osu_python.classes import config
from os.path import isdir

cursor_img = None
trail_img = None
cursor_middle_img = None

def load_skin():
    global cursor_img, trail_img, cursor_middle_img
    try:
        path = config.base_path + "/skins/" + config.cfg["skin"]
        if not isdir(path):
            path = "./skin"
    except KeyError:
        path = "./skin"

    cursor_img = pg.image.load(path + "/cursor.png").convert_alpha()
    trail_img = pg.image.load(path + "/cursortrail.png").convert_alpha()
    try:
        cursor_middle_img = pg.image.load(path + "/cursormiddle.png").convert_alpha()
    except FileNotFoundError:
        pass

    try:
        Cursor.rotation = config.skin_ini["[General]"]["CursorRotate"]
    except KeyError:
        pass


class Cursor:
    def __init__(self, scale):
        load_skin()

        self.sizes = (
            cursor_img.get_width() * scale,
            cursor_img.get_height() * scale,
        )
        self.cursor_img = pg.transform.scale(cursor_img, self.sizes)

        self.trail_sizes = (
            trail_img.get_width() * scale,
            trail_img.get_height() * scale,
        )
        self.trail_img = pg.transform.scale(trail_img, self.trail_sizes)

        self.cursor_middle_img = None
        if cursor_middle_img:
            self.cursor_middle_sizes = (

            )
            