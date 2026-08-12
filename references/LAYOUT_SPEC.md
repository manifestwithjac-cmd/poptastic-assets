# Poptastic listing layout spec

The visual target is `assets/LAYOUT_REFERENCE.jpg`. Every Poptastic main listing image uses
this identical skeleton — only the theme art, palette, and copy change. Consistency across the
shop is the point: a browsing customer should recognize a Poptastic listing from the grid view
before reading a word.

## Canvas

2000 × 2000 px, PNG, sRGB. Etsy's recommended main listing size; it stays crisp when Etsy
generates its own thumbnails.

## Grid

Five panels on a soft off-white page, each panel a white rounded card with generous padding.

```
┌──────────────────────────────────────────────────┐
│  ✦        HEADER — KIT TITLE IN CAPS         ✦   │  ~9% height
├───────────────────────────────┬──────────────────┤
│                               │                  │
│      CLASSIC KIT PICTURED     │  BALLOON TOWER   │  ~58% height
│      (hero scene photo)       │                  │
│                               │  BALLOON TOWER   │
│                               │  INCLUDES:       │
├──────────────┬────────────────┼──────────────────┤
│ FOIL BOUQUET │ BALLOON BOUQUET│ INCLUDED COLORS  │  ~31% height
│              │   LATEX ONLY   │    & FOILS       │
│  INCLUDES:   │   INCLUDES:    │  ● ● ● ●         │
│              │                │  foil cutouts    │
└──────────────┴────────────────┴──────────────────┘
```

Left column of the main row is ~65% of the width. Bottom row splits roughly 32 / 30 / 38.

## Type

All caps headers in the accent color, bold, tight tracking. Body copy in the same family,
regular weight, dark neutral. Bulleted "INCLUDES:" lists sit under the panel title or beneath
the photo depending on panel height.

| Element | Weight | Size @2000px | Color |
|---|---|---|---|
| Header title | Bold | ~72 px | accent |
| Panel title | Bold | ~40 px | accent |
| "INCLUDES:" label | Bold | ~30 px | accent |
| Bullet items | Regular | ~26 px | near-black |
| Swatch / foil labels | Regular | ~22 px | near-black |
| Disclaimer | Bold | ~24 px | accent |

Default family is Outfit. To match the shop's exact brand font, drop the TTF into
`assets/fonts/` and set `font_bold` / `font_regular` in the kit spec.

## Color

- Page background: very soft off-white, faintly tinted toward the theme
- Panel cards: pure white, so white-background product photos blend edge to edge
- Accent: the kit's brand accent, used for every header and the disclaimer. Deep purple is the
  Poptastic default; a theme may shift it, but only one accent per graphic.

## Copy rules

These are product claims, not decoration. A customer buys against them.

- Header is the kit name in caps, ending in "BALLOON KIT".
- Panel titles are fixed: `CLASSIC KIT PICTURED`, `BALLOON TOWER`, `FOIL BOUQUET`,
  `BALLOON BOUQUET LATEX ONLY`, `INCLUDED COLORS & FOILS`.
- Bullet counts must match the kit spec exactly. Never round, never guess.
- Foil balloons are named in parentheses: `1 Foil Balloon (Number 1)`, or the shape's own
  name when the kit is topped by a themed foil instead: `1 Foil Balloon (Lemon Slice)`.
- Color names are customer-facing and may pair a plain name with a descriptor:
  `Blossom (Purple)`, `Pale Yellow (Ivory)`, `Eucalyptus (Green)`. Spell-check every one.
- When florals and greenery are excluded — nearly always — the disclaimer appears in the hero
  panel: `*NO GREENERY OR FLORALS INCLUDED, BALLOONS ONLY.`

## Panel photography briefs

Every panel is generated with the garland reference attached and the palette named explicitly.

**Hero — classic kit pictured.** A styled room scene: arched backdrop panel, the organic
garland climbing its left edge and spilling across the top, plus a small separate floor cluster
to the right of the backdrop. Theme foils tucked into the garland. Natural diffused daylight,
real interior, shot like an event photograph. Governed entirely by `GARLAND_LAW.md`.

**Balloon tower.** The number foil standing on a tiered base of latex balloons, pure white
background, soft contact shadow, straight-on product photography.

**Foil bouquet.** The number foil plus the stated latex count, ribbons gathered into a foil
balloon weight at the base, pure white background.

**Latex bouquet.** The stated latex count only, no foils, ribbons into a weight, pure white
background.

**Foil cutouts.** Each foil shape photographed alone, straight on, pure white background, no
shadow beyond a whisper. These sit in the colors and foils grid beneath their labels.

## Proof before delivering

- [ ] Every word spelled correctly, color names especially
- [ ] Bullet counts match the kit spec
- [ ] Swatch count matches the number of latex colors
- [ ] Swatch hex values visually match the balloons in the photos
- [ ] Each foil label sits under the correct foil
- [ ] Disclaimer present when florals are excluded
- [ ] Nothing clipped at a panel edge
- [ ] Balloon colors across all panels are consistent with each other
