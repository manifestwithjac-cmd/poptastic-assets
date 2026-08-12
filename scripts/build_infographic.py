#!/usr/bin/env python3
"""Composite the generated panels and the kit copy into the final listing image.

All text is drawn here with real fonts and real hex values, which is why the
typography is exact instead of whatever an image model felt like spelling.

Usage:
    python3 scripts/build_infographic.py kits/my-kit.json \
        --panels work/my-kit/ --out output/my-kit.png

Panels that have not been generated yet render as labelled placeholders, so the
layout and all copy can be proofed before spending anything on images.
"""
import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from layout import CANVAS, CARD_PAD, CARD_RADIUS, HEADER_H, MARGIN, cards, photo_boxes  # noqa: E402

WHITE = (255, 255, 255)
INK = (44, 38, 52)
MUTED = (150, 143, 158)

TITLE_SIZE = 72
PANEL_TITLE_SIZE = 40
INCLUDES_SIZE = 30
BULLET_SIZE = 26
LABEL_SIZE = 22
DISCLAIMER_SIZE = 24


# --------------------------------------------------------------------------- utils

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def load_font(path, size):
    try:
        return ImageFont.truetype(str(path), size)
    except Exception:
        return ImageFont.load_default(size)


def text_size(draw, text, font):
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]


def fit_font(draw, text, font_path, max_width, start_size, min_size=12):
    """Shrink a font until the text fits the width. Long kit names happen."""
    size = start_size
    while size > min_size:
        font = load_font(font_path, size)
        if text_size(draw, text, font)[0] <= max_width:
            return font
        size -= 2
    return load_font(font_path, min_size)


def wrap(draw, text, font, max_width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if text_size(draw, trial, font)[0] <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, text, font, cx, y, fill):
    w, _ = text_size(draw, text, font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)
    return y


def paste_contain(canvas, img_path, box, placeholder_label=None):
    """Fit an image inside a box, centred, preserving aspect ratio."""
    x, y, w, h = box
    if img_path is None or not Path(img_path).exists():
        d = ImageDraw.Draw(canvas)
        d.rounded_rectangle([x, y, x + w, y + h], radius=14,
                            outline=(226, 220, 232), width=3)
        if placeholder_label:
            f = load_font(ROOT / "assets/fonts/Outfit-Regular.ttf", 22)
            tw, th = text_size(d, placeholder_label, f)
            d.text((x + w / 2 - tw / 2, y + h / 2 - th / 2), placeholder_label,
                   font=f, fill=MUTED)
        return

    img = Image.open(img_path).convert("RGB")
    scale = min(w / img.width, h / img.height)
    new = img.resize((max(1, int(img.width * scale)), max(1, int(img.height * scale))),
                     Image.LANCZOS)
    canvas.paste(new, (int(x + (w - new.width) / 2), int(y + (h - new.height) / 2)))


def draw_bullets(draw, items, x, y, max_width, font_bold, font_reg, accent,
                 label="INCLUDES:", line_gap=12, label_size=INCLUDES_SIZE,
                 item_size=BULLET_SIZE):
    f_label = fit_font(draw, label, font_bold, max_width, label_size)
    f_item = load_font(font_reg, item_size)
    draw.text((x, y), label, font=f_label, fill=accent)
    y += label_size + 14
    for item in items:
        for i, line in enumerate(wrap(draw, item, f_item, max_width - 26)):
            if i == 0:
                draw.ellipse([x + 4, y + item_size / 2 - 3,
                              x + 10, y + item_size / 2 + 3], fill=INK)
            draw.text((x + 22, y), line, font=f_item, fill=INK)
            y += item_size + line_gap
    return y


# --------------------------------------------------------------------------- panels

def draw_card(draw, rect):
    x, y, w, h = rect
    draw.rounded_rectangle([x, y, x + w, y + h], radius=CARD_RADIUS, fill=WHITE)


def panel_title(draw, text, rect, font_bold, accent, size=PANEL_TITLE_SIZE):
    x, y, w, _ = rect
    font = fit_font(draw, text, font_bold, w - 2 * CARD_PAD, size)
    draw_centered(draw, text, font, x + w / 2, y + 14, accent)


def build(kit, panels_dir, out_path):
    accent = hex_to_rgb(kit.get("accent_hex", "#5B1A9E"))
    page_bg = hex_to_rgb(kit.get("page_bg_hex", "#F7F3F9"))
    fb = ROOT / kit.get("font_bold", "assets/fonts/Outfit-Bold.ttf")
    fr = ROOT / kit.get("font_regular", "assets/fonts/Outfit-Regular.ttf")

    panels_dir = Path(panels_dir) if panels_dir else None

    def panel(name):
        if panels_dir is None:
            return None
        p = panels_dir / f"{name}.png"
        return p if p.exists() else None

    canvas = Image.new("RGB", (CANVAS, CANVAS), page_bg)
    draw = ImageDraw.Draw(canvas)
    rects, boxes = cards(), photo_boxes()

    # ---- header
    title = kit["header_title"]
    f_title = fit_font(draw, title, fb, CANVAS - 2 * MARGIN - 300, TITLE_SIZE)
    _, th = text_size(draw, title, f_title)
    draw_centered(draw, title, f_title, CANVAS / 2, (HEADER_H - th) / 2 - 8, accent)

    for side, box in (("header_art_left", (MARGIN + 10, 10, 190, HEADER_H - 20)),
                      ("header_art_right", (CANVAS - MARGIN - 200, 10, 190, HEADER_H - 20))):
        p = panel(side)
        if p:
            paste_contain(canvas, p, box)

    # ---- hero
    r = rects["hero"]
    draw_card(draw, r)
    panel_title(draw, "CLASSIC KIT PICTURED", r, fb, accent, 44)
    paste_contain(canvas, panel("hero"), boxes["hero"], "hero.png — not generated yet")

    if not kit.get("florals_included") and kit.get("disclaimer"):
        hx, hy, hw, hh = boxes["hero"]
        f_dis = load_font(fb, DISCLAIMER_SIZE)
        lines = wrap(draw, kit["disclaimer"], f_dis, hw * 0.5)
        pill_h = len(lines) * (DISCLAIMER_SIZE + 8) + 24
        pill_w = max(text_size(draw, ln, f_dis)[0] for ln in lines) + 44
        px = hx + hw - pill_w - 24
        py = hy + hh - pill_h - 20
        draw.rounded_rectangle([px, py, px + pill_w, py + pill_h], radius=14,
                               fill=(255, 255, 255))
        ty = py + 12
        for ln in lines:
            draw_centered(draw, ln, f_dis, px + pill_w / 2, ty, accent)
            ty += DISCLAIMER_SIZE + 8

    # ---- tower
    r = rects["tower"]
    draw_card(draw, r)
    tw = kit["panels"]["tower"]
    panel_title(draw, tw["title"], r, fb, accent)
    paste_contain(canvas, panel("tower"), boxes["tower"], "tower.png")
    bx, by, bw, bh = boxes["tower"]
    draw_bullets(draw, tw["includes"], r[0] + CARD_PAD + 6, by + bh + 24,
                 r[2] - 2 * CARD_PAD, fb, fr, accent,
                 label=f"{tw['title']} INCLUDES:")

    # ---- the two bouquet panels
    for key in ("foil_bouquet", "latex_bouquet"):
        r = rects[key]
        spec = kit["panels"][key]
        draw_card(draw, r)
        panel_title(draw, spec["title"], r, fb, accent, 34)
        paste_contain(canvas, panel(key), boxes[key], key)
        px, py, pw, _ = boxes[key]
        text_x = px + pw + 18
        text_w = r[0] + r[2] - CARD_PAD - text_x
        draw_bullets(draw, spec["includes"], text_x, py + 54, text_w, fb, fr, accent,
                     label_size=26, item_size=23, line_gap=10)

    # ---- colors and foils
    r = rects["colors"]
    draw_card(draw, r)
    panel_title(draw, "INCLUDED COLORS & FOILS", r, fb, accent, 36)

    cx0, cy0, cw, ch = r
    inner_x = cx0 + CARD_PAD
    inner_w = cw - 2 * CARD_PAD
    y = cy0 + 92

    palette = kit["palette"]
    per_row = min(4, max(1, len(palette)))
    cell_w = inner_w / per_row
    dot = int(min(96, cell_w * 0.62))
    f_label = load_font(fr, LABEL_SIZE)

    for i, color in enumerate(palette):
        row, col = divmod(i, per_row)
        ccx = inner_x + cell_w * (col + 0.5)
        ccy = y + row * (dot + 78)
        draw.ellipse([ccx - dot / 2, ccy, ccx + dot / 2, ccy + dot],
                     fill=hex_to_rgb(color["hex"]))
        ly = ccy + dot + 10
        for line in wrap(draw, color["name"], f_label, cell_w - 8):
            draw_centered(draw, line, f_label, ccx, ly, INK)
            ly += LABEL_SIZE + 4

    rows = (len(palette) + per_row - 1) // per_row
    y += rows * (dot + 78) + 6
    draw.line([inner_x + 20, y, cx0 + cw - CARD_PAD - 20, y], fill=(230, 224, 236), width=2)
    y += 22

    foils = kit.get("foils", [])
    if foils:
        fcols = min(3, len(foils))
        fcell = inner_w / fcols
        avail_h = cy0 + ch - CARD_PAD - y - 56
        for i, foil in enumerate(foils):
            col = i % fcols
            fx = inner_x + fcell * col
            paste_contain(canvas, panel(f"foil_{i}"),
                          (int(fx + 8), int(y), int(fcell - 16), int(avail_h)),
                          f"foil_{i}")
            ly = y + avail_h + 8
            for line in wrap(draw, foil["label"], f_label, fcell - 10):
                draw_centered(draw, line, f_label, fx + fcell / 2, ly, INK)
                ly += LABEL_SIZE + 4

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path, "PNG")
    return out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kit")
    ap.add_argument("--panels", default=None,
                    help="directory of generated panels; omit to preview the layout only")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    kit = json.loads(Path(args.kit).read_text())
    path = build(kit, args.panels, args.out)
    print(f"Wrote {path}")
    print("Proof it against the checklist in references/LAYOUT_SPEC.md before delivering.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
