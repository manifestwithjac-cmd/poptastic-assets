"""Shared geometry for the Poptastic listing infographic.

Both the panel generator and the compositor import this so the images are
generated at exactly the aspect ratio of the box they will land in. Change the
grid here and both stages follow.
"""

CANVAS = 2000
MARGIN = 24
GUTTER = 20
CARD_PAD = 20
CARD_RADIUS = 22

HEADER_H = 156
ROW1_TOP = HEADER_H + GUTTER
ROW1_H = 1168
ROW2_TOP = ROW1_TOP + ROW1_H + GUTTER
ROW2_H = CANVAS - MARGIN - ROW2_TOP

_INNER = CANVAS - 2 * MARGIN  # 1952

# Row 1: hero on the left, tower on the right.
HERO_W = 1312
TOWER_W = _INNER - HERO_W - GUTTER

# Row 2: two bouquet panels and the colors grid.
FOIL_BQ_W = 640
LATEX_BQ_W = 640
COLORS_W = _INNER - FOIL_BQ_W - LATEX_BQ_W - 2 * GUTTER


def cards():
    """Panel rectangles as (x, y, w, h) in canvas pixels."""
    x = MARGIN
    hero = (x, ROW1_TOP, HERO_W, ROW1_H)
    tower = (x + HERO_W + GUTTER, ROW1_TOP, TOWER_W, ROW1_H)

    foil_bq = (x, ROW2_TOP, FOIL_BQ_W, ROW2_H)
    latex_bq = (x + FOIL_BQ_W + GUTTER, ROW2_TOP, LATEX_BQ_W, ROW2_H)
    colors = (x + FOIL_BQ_W + LATEX_BQ_W + 2 * GUTTER, ROW2_TOP, COLORS_W, ROW2_H)

    return {
        "hero": hero,
        "tower": tower,
        "foil_bouquet": foil_bq,
        "latex_bouquet": latex_bq,
        "colors": colors,
    }


# Title bar height reserved inside each card, and how the photo shares the card.
TITLE_H = {"hero": 58, "tower": 54, "foil_bouquet": 50, "latex_bouquet": 50, "colors": 54}

# Bottom-row bouquet panels put the photo on the left and the includes list on the right.
BQ_PHOTO_FRACTION = 0.40


def photo_boxes():
    """Where the generated photo sits inside each card, as (x, y, w, h)."""
    c = cards()
    out = {}

    x, y, w, h = c["hero"]
    out["hero"] = (x + CARD_PAD, y + TITLE_H["hero"],
                   w - 2 * CARD_PAD, h - TITLE_H["hero"] - CARD_PAD)

    # Tower reserves room under the photo for its INCLUDES list.
    x, y, w, h = c["tower"]
    out["tower"] = (x + CARD_PAD, y + TITLE_H["tower"],
                    w - 2 * CARD_PAD, h - TITLE_H["tower"] - 250)

    for key in ("foil_bouquet", "latex_bouquet"):
        x, y, w, h = c[key]
        pw = int((w - 2 * CARD_PAD) * BQ_PHOTO_FRACTION)
        out[key] = (x + CARD_PAD, y + TITLE_H[key],
                    pw, h - TITLE_H[key] - CARD_PAD)

    return out


def snap_size(w, h, min_px=655_360, max_px=8_294_400, max_edge=3840):
    """Round a desired panel size to something gpt-image-2 will accept.

    The API requires both edges to be multiples of 16, a long:short ratio no
    worse than 3:1, at least 655,360 total pixels and at most 8,294,400, with no
    edge over 3840. Small panels get scaled up proportionally and downsampled by
    the compositor, which also gives cleaner detail than generating them tiny.
    """
    w, h = float(w), float(h)

    # Ratio clamp first, otherwise scaling can't fix it.
    ratio = max(w, h) / min(w, h)
    if ratio > 3.0:
        if w > h:
            h = w / 3.0
        else:
            w = h / 3.0

    def _round16(v):
        return max(16, int(round(v / 16.0)) * 16)

    for _ in range(24):
        rw, rh = _round16(w), _round16(h)
        total = rw * rh
        if total < min_px:
            w, h = w * 1.06, h * 1.06
            continue
        if total > max_px or max(rw, rh) > max_edge:
            w, h = w * 0.94, h * 0.94
            continue
        return rw, rh

    return _round16(w), _round16(h)


def generation_sizes():
    """The size to request from the API for each generated panel."""
    boxes = photo_boxes()
    sizes = {k: snap_size(b[2], b[3]) for k, b in boxes.items() if k != "colors"}
    sizes["foil"] = (1024, 1024)  # each foil cutout, square
    return sizes


if __name__ == "__main__":
    for name, box in photo_boxes().items():
        print(f"{name:<14} box={box}")
    print()
    for name, size in generation_sizes().items():
        w, h = size
        print(f"{name:<14} request={w}x{h}  px={w*h:,}  ratio={max(w,h)/min(w,h):.2f}")
