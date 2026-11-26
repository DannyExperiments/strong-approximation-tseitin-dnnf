"""Render a rotating four-syndrome example and its offline explorer bundle."""

import math
import os
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FONT_DIR = Path(os.environ.get("Q515_FONT_DIR", "/System/Library/Fonts/Supplemental"))
BG, PANEL, WHITE, MUTED = "#10182c", "#1d2a42", "#f4f7ff", "#c8d5e9"
TEAL, GOLD, GREY = "#65dcb5", "#ffc473", "#394c6d"
SYMBOLS = ("00", "01", "10", "11")
DIAGONAL = {(i, i) for i in range(4)}
FIRST, SECOND = {(0, 1), (1, 1)}, {(0, 0), (0, 1)}
SQUARE = {(i, j) for i in (0, 1) for j in (0, 1)}
STATES = (
    ("Matching syndromes", ("4 true diagonal cells.", "A pair is true when A and B agree.")),
    ("Overlapping rectangles", ("Both include false pair (00, 01).", "2 appearances, 1 distinct false pair.")),
    ("A single 2 × 2 rectangle", ("2 true cells and 2 false cells.", "t² = 4 = L·|R|, with L = 1.")),
)


def font(size, bold=False):
    file = "Arial Bold.ttf" if bold else "Arial.ttf"
    return ImageFont.truetype(str(FONT_DIR / file), size)


def project(col, row, z, angle):
    x, y = col - 2, row - 2
    u, v = math.cos(angle), math.sin(angle)
    return round(352 + 104 * (u * x - v * y)), round(352 + 60 * (v * x + u * y) - 53 * z)


def tile(draw, row, col, height, colour, angle):
    x, y = col + .055, row + .055
    opposite_x, opposite_y = x + .89, y + .89
    top = [project(v, w, height, angle) for v, w in
           ((x,y), (opposite_x,y), (opposite_x,opposite_y), (x,opposite_y))]
    bottom = [project(v, w, 0, angle) for v, w in
              ((x,y), (opposite_x,y), (opposite_x,opposite_y), (x,opposite_y))]
    if height:
        side = "#287c71" if colour == TEAL else "#99602d"
        draw.polygon([top[1],top[2],bottom[2],bottom[1]], fill=side)
        draw.polygon([top[2],top[3],bottom[3],bottom[2]], fill=side)
    draw.polygon(top, fill=colour)


def render_frame(state, angle):
    image = Image.new("RGB", (704, 835), BG)
    draw = ImageDraw.Draw(image)
    draw.text((34, 29), "Syndrome rectangles", font=font(52, True), fill=WHITE)
    draw.text((36, 96), "A four-syndrome equality example", font=font(33), fill=MUTED)
    draw.rounded_rectangle((31, 153, 673, 574), radius=25, fill=PANEL)

    for row, col in sorted(((i,j) for i in range(4) for j in range(4)),
                           key=lambda pair: math.sin(angle)*pair[1] + math.cos(angle)*pair[0]):
        cell = (row,col)
        if state == 0:
            height = .58 if cell in DIAGONAL else 0
        elif state == 1:
            height = .68 * ((cell in FIRST) + (cell in SECOND))
        else:
            height = .78 if cell in SQUARE else 0
        colour = TEAL if cell in DIAGONAL else GOLD if height else GREY
        tile(draw, row, col, height, colour, angle)

    for i, symbol in enumerate(SYMBOLS):
        x, y = project(i+.5,4.29,0,angle)
        draw.text((x,y),symbol,font=font(27,True),fill=MUTED,anchor="mm")
        x, y = project(4.34,i+.5,0,angle)
        draw.text((x,y),symbol,font=font(27,True),fill=MUTED,anchor="mm")
    x,y = project(2,4.82,0,angle)
    draw.text((x,y),"B",font=font(29,True),fill=MUTED,anchor="mm")
    x,y = project(4.80,2,0,angle)
    draw.text((x,y),"A",font=font(29,True),fill=MUTED,anchor="mm")
    for x, colour, label in ((53,TEAL,"True pair"),(329,GOLD,"Accepted false pair")):
        draw.rounded_rectangle((x,532,x+23,555),radius=4,fill=colour)
        draw.text((x+35,528),label,font=font(27,True),fill=WHITE)

    title, captions = STATES[state]
    draw.text((34,596),title,font=font(44,True),fill=WHITE)
    draw.line(((35,665),(670,665)),fill=GREY,width=2)
    for i, caption in enumerate(captions):
        draw.text((36,689+i*49),caption,font=font(33),fill=WHITE)
    return image.quantize(colors=48,method=Image.Quantize.MEDIANCUT)


def main():
    frames, duration = [], []
    for state in range(3):
        for step in range(20):
            angle = .46 + .15 * math.sin(math.tau * step / 20)
            frames.append(render_frame(state, angle))
            duration.append(250 if step == 0 else 170)
    frames[0].save(HERE / "syndrome-rectangles.gif", save_all=True,
                   append_images=frames[1:],duration=duration,disposal=1,loop=0,optimize=True)
    archive_member = ZipInfo("index.html", (1980,1,1,0,0,0))
    archive_member.create_system = 3
    archive_member.external_attr = 0o100644 << 16
    with ZipFile(HERE / "syndrome-rectangles-explorer.zip", "w") as archive:
        archive.writestr(archive_member,(HERE / "index.html").read_bytes(),ZIP_DEFLATED,compresslevel=9)


if __name__ == "__main__":
    main()
