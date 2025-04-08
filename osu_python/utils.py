import typing as t
import pygame as pg
import os


def calculate_fade_in(ar: float) -> float:
    #calculates fade_in time from AR
    if ar < 5:
        return 800 + 400 * (5 - ar) / 5
    if ar == 5:
        return 800
    if ar > 5:
        return 800 - 500 * (ar - 5) / 5


def calculate_preempt(ar: float) -> float:
    #calculates preempt from AR
    if ar < 5:
        return 1200 + 600 * (5 - ar) / 5
    if ar == 5:
        return 1200
    if ar > 5:
        return 1200 - 750 * (ar - 5) / 5


def calculate_hit_r(cs: float) -> float:
    return 54.4 - 4.48 * cs


def calculate_appr_r(cs: float) -> float:
    return calculate_hit_r(cs) * 2


def playfield_size(h:int) -> t.Tuple[int, int]:
    return ((4 / 3) * h * 0.9, h * 0.9)


def osu_scale(n: int) -> float:
    return n / 480


def calculate_hit_windows(od: float) -> t.Tuple[int, int, int]:
    return (80 - 6 * od, 140 - 8 * od, 200 - 10 * od)


def calculate_accuracy(scores: t.Tuple[int, int, int, int]) -> float:
    s300, s100, s50, _ = scores
    try:
        accuracy = (s300 * 300 + s100 * 100 + s50 * 50) / (300 * sum(scores))
    except ZeroDivisionError:
        accuracy = 1.0
    return accuracy


def calculate_difficulty_multiplier(
    HP: float, CS: float, OD: float, hit_objects_count: int, drain_time: float):
    return round(
        HP + CS + OD + max(min(hit_objects_count / drain_time * 8, 16), 0) / 38 * 5)


def convert_type(value: str):
    value.split("//")[0]
    try:
        return int(value)
    except ValueError:
        pass

    l_values = value.split(",")
    length = len(l_values)
    if length != 1:
        return [convert_type(value) for v in l_values]
    return value.strip()


def parse_ini(path: os.PathLike):
    f = open(path, encoding="utf-8-sig")
    all_lines = f.readlines()
    category = None
    output = {"No category": []}
    for line in all_lines:
        if len(line) < 2:
            continue
        if line[0] == "[":
            category = line.strip()
            output[category] = {}
            continue
        if line[:2] == "//":
            continue
        try:
            key, value = line.split(":")
        except ValueError:
            if category == None:
                output["No category"].append(line.strip())
            continue
        key = key.strip()
        value = value.strip()
        if category != None:
            output[category][key] = convert_type(value)
        else:
            output["No category"].append(line)
        return output


def parse_additional_info(path: os.PathLike):
    f = open(path, encoding="utf-8-sig")
    all_lines = f.readlines()
    category = None
    colours = []
    obj_types = []
    for line in all_lines:
        if line.strip() == "[Colours]":
            category = "[Colours]"
            continue
        if line.strip() == "[HitObjects]":
            category = "[HitObjects]"
            continue
        if category == "Colours" and line.strip().startswith("Combo"):
            try:
                colour = line.split(":")[1]
                colour.append(convert_type(colour))
            except IndexError:
                continue
        if category == "[HitObjects]":
            if line.startswith("["):
                break
            obj_type = line.split(",")[3]
            obj_types.append(int(obj_type))
    return colours, obj_types


def chunks(lst, n):
    return [lst[i::n] for i in range(n)]

def fit_image_to_screen(image: pg.Surface, size: t.Tuple[int, int]):
    WIDTH = 0
    HEIGHT = 1
    bg = image.get_size()
    smaller_side = WIDTH if bg[WIDTH] < bg[HEIGHT] else HEIGHT
    scale = size[smaller_side] / bg[smaller_side]
    ns = (bg[WIDTH] * scale, bg[HEIGHT] * scale)
    if ns[WIDTH] < size[WIDTH]:
        coeff = size[WIDTH] / ns[WIDTH]
        ns = (ns[0] * coeff, ns[1] * coeff)
    return pg.transform.scale(image, ns)


def inside_a_circle(x, y, c_x, c_y, r) -> bool:
    return (x - c_x) ** 2 + (y - c_y) ** 2 < r ** 2


def calculate_rank(accuracy) -> str:
    if accuracy == 1:
        return "X"
    elif accuracy >= 0.95:
        return "S"
    elif accuracy >= 0.90:
        return "A"
    elif accuracy >= 0.80:
        return "B"
    elif accuracy >= 0.70:
        return "C"
    else:
        return "D"







