import pygame as pg
from osu_python import utils
import typing as t
from osu_python.classes import config


score_imgs = None
hp_bar_bg_img = None
hp_bar_colour_img = None
hp_bar_marker_img = None
score_overlap = 0
combo_overlap = 0


def load_skin():
    global score_imgs, hp_bar_colour_img, hp_bar_bg_img, hp_bar_marker_img, score_overlap, combo_overlap
    path = config.base_path + "/skins/" + config.cfg["skin"]
    score_path = (
        path + "/" + config.skin_ini["[Fonts]"]["ScorePrefix"].replace("\\", "/")
    )

    score_imgs = {
        "0": pg.image.load(score_path + "-0.png").convert_alpha(),
        "1": pg.image.load(score_path + "-1.png").convert_alpha(),
        "2": pg.image.load(score_path + "-2.png").convert_alpha(),
        "3": pg.image.load(score_path + "-3.png").convert_alpha(),
        "4": pg.image.load(score_path + "-4.png").convert_alpha(),
        "5": pg.image.load(score_path + "-5.png").convert_alpha(),
        "6": pg.image.load(score_path + "-6.png").convert_alpha(),
        "7": pg.image.load(score_path + "-7.png").convert_alpha(),
        "8": pg.image.load(score_path + "-8.png").convert_alpha(),
        "9": pg.image.load(score_path + "-9.png").convert_alpha(),
        ".": pg.image.load(score_path + "-dot.png").convert_alpha(),
        "%": pg.image.load(score_path + "-percent.png").convert_alpha(),
        "x": pg.image.load(score_path + "-x.png").convert_alpha(),
    }

    hp_bar_bg_img = pg.image.load(path + "/scorebar-bg.png").convert_alpha()
    hp_bar_colour_img = pg.image.load(path + "/scorebar-colour.png").convert_alpha()
    try:
        hp_bar_marker_img = pg.image.load(path + "/scorebar-marker.png").convert_alpha()
    except FileNotFoundError:
        pass

    try:
        score_overlap = config.skin_ini["[Fonts]"]["ScoreOverlap"]
    except KeyError:
        pass

    try:
        combo_overlap = config.skin_ini["[Fonts]"]["ComboOverlap"]
    except KeyError:
        pass


    class InGameUI:
        def __init__(
                self,
                difficulty_multiplier: int,
                mod_multiplier: float,
                background: pg.Surface,
                background_dim: float,
                monitor_size: t.Tuple[int, int],
                HP: float,
                current_time: int,
        ) -> None:

            self.score = 0
            self.display_score = 0
            self.combo = 0
            self.max_combo = 0
            self.accuracy = 1.00
            self.hp = 1
            self.map_hp = HP
            self.last_hp_drain = current_time

            self.scores = {"300": 0, "100": 0, "50": 0, "0": 0}

            self.difficulty_multiplier = difficulty_multiplier
            self.mod_multiplier = mod_multiplier

            self.raw_background = utils.fit_image_to_screen(background, monitor_size)
            self.bg_dim = background_dim
            self.background = self.get_dimmed_bg().convert_alpha()

            full_width = 0
            for n in range(10):
                full_width += score_imgs[str(n)].get_width()
            self.num_gap = full_width / 10 + 1