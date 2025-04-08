import pygame as pg
import sys
from screeninfo import get_monitors
import logging
from datetime import datetime
import typing as t


TIME_GO_IN = 0


for m in get_monitors():
    if m.is_primary:
        width, height = m.width, m.height
pg.display.init()
screen = pg.display.set_mode((width, height), flags=pg.FULLSCREEN | pg.DOUBLEBUF)

from osu_python import classes, scenes, map_loader



