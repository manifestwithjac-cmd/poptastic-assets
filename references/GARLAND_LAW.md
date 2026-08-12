# Garland Law

How a real organic balloon garland is built, and how to tell when the model got it wrong.
`assets/GARLAND_REFERENCE.png` is the authoritative photo. Match its **construction** —
never its colors, theme, backdrop, or room.

## Contents

1. Size hierarchy
2. Path and silhouette
3. Mini quads
4. Latex realism
5. Depth and occlusion
6. Florals
7. The reject list

---

## 1. Size hierarchy

Only three readable sizes exist. Intermediate sizes make the garland look computer-generated,
because a real installer buys balloons in three packs, not a smooth gradient.

| Category | Real size | Role |
|---|---|---|
| SMALL | ~5 in | accent only, ~half the diameter of a standard or less |
| STANDARD | ~10–11 in | the structural backbone |
| LARGE | ~16–18 in | occasional accent, 1.5–1.7× a standard |

**Standard balloons must visually dominate.** A viewer should immediately read the standard
balloons as the backbone. They run consecutively through large stretches of the garland:

```
STANDARD · STANDARD · STANDARD · STANDARD · mini quad · STANDARD · STANDARD ·
occasional LARGE · STANDARD · STANDARD · STANDARD
```

Not this, which is the most common failure:

```
LARGE · STANDARD · LARGE · STANDARD · LARGE · STANDARD
```

**Hard cap: roughly 4–5 visibly oversized balloons in a full 10-foot garland.** No more. They
are separated by several standards, never placed beside each other, and never used to build a
base. Nothing should read as a 24-inch or 36-inch balloon.

## 2. Path and silhouette

The garland does not climb in a straight vertical column and it does not sit on a triangular
foundation.

- It meanders: slightly inward, then outward, then inward again as it climbs.
- Some clusters project outward from the backdrop; some tuck back against it; some spill
  slightly across its face.
- No visible straight central axis.
- The bottom simply begins at floor level and continues organically upward. It is only
  slightly wider than the sections near it. No symmetrical foundation, no three giant balloons
  forming a base, no bottom-heaviness.
- The outer contour is interrupted — individual standards poke out, shallow valleys open
  between balloons, the width goes narrow, fuller, narrow again. A consistent diameter reads
  as machine-made.

## 3. Mini quads

The 5-inch balloons appear as **distinct four-balloon clusters**, roughly 5–7 of them across a
full garland, each reading as one tight little four-petal group attached to the larger
structure.

They are never scattered as individuals, never in pairs, and never used as a gradual
transition size. Substantial stretches of the garland carry no small balloons at all.

## 4. Latex realism

This is what separates the reference photo from a render.

**Shape.** Real inflated latex is not a perfect sphere. Standards vary in width, height,
orientation, and inflation. Some read subtly oval or pear-shaped. Some face camera, some turn
sideways, some sit partly hidden. No two balloons share identical geometry.

**Light.** The single biggest CGI tell is the same small white oval highlight stamped on every
balloon. Reflections must change with orientation: a broad soft window reflection on one, a
barely-there highlight on another, almost nothing on a balloon facing away from the light,
neighboring balloons reflected in a third. Highlights differ in size, position, intensity,
shape, and softness. Broad diffused environmental reflections, not identical shine marks.

The target is real latex photographed in natural diffused daylight — not rendered plastic.

## 5. Depth and occlusion

Real garlands hide balloons behind other balloons. Visibility should range across roughly 30%,
50%, 70%, and fully visible. Without genuine overlap the installation reads as separate
circles arranged on a flat plane.

## 6. Florals

Poptastic kits are balloons only. Florals appear only when explicitly requested as styling,
and then:

- **Exactly three** small placements on the main garland — one in the upper third, one around
  the middle, one in the lower third. No more.
- Each arrangement smaller than a single standard balloon, tucked into the garland.
- **Absolutely none on the right-side floor cluster.** That cluster is latex only.
- The graphic carries the "no greenery or florals included, balloons only" disclaimer.

## 7. The reject list

Compare the generated hero against the reference before accepting it. Regenerate if any of
these are true:

- [ ] Oversized balloons dominate, or more than ~5 of them
- [ ] The bottom forms a wide triangular base
- [ ] The garland reads as a vertical column or has a straight central axis
- [ ] Small balloons are scattered individually instead of forming quads
- [ ] Standard 10–11 in balloons are not clearly the dominant size
- [ ] Mini quads are not readable as four-balloon groups
- [ ] The silhouette is smooth, uniform, or mathematically even
- [ ] The garland is excessively dense
- [ ] The same white highlight repeats across balloons
- [ ] Balloons look perfectly spherical and computer-rendered
- [ ] The garland does not meander
- [ ] Flowers appear on the right-side floor cluster
- [ ] Any balloon color is outside the kit palette

When regenerating, append the specific failure as a correction note rather than re-rolling the
same prompt — the model responds far better to "the bottom has become a wide triangular base,
remove it" than to another identical attempt.
