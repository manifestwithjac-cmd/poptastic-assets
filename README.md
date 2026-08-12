# Poptastic Party Shop — shared assets

Reference images for balloon-kit listing infographics.

| File | What it is |
|---|---|
| `cherry-foil.png` | Cherry foil balloon (two red cherries, green stem) |
| `daisy-foil.png` | Daisy foil balloon (white petals, yellow center) |
| `color-chart1.webp` | Latex swatch chart 1 (blues, purples, pinks, browns, neutrals) |
| `color-chart2.webp` | Latex swatch chart 2 (reds, yellows, greens, blues) |

Raw URL pattern:
`https://raw.githubusercontent.com/manifestwithjac-cmd/poptastic-assets/main/<file>`

## Kit infographics

Each Poptastic balloon-kit listing image is driven by one JSON spec in `kits/`.
Adding or changing a kit JSON triggers the **Render kit infographic** GitHub
Action (`.github/workflows/render-kit.yml`), which generates the balloon panels
via OpenAI `gpt-image-2`, composites the 2000×2000 listing graphic in code, and
commits the result to `output/<kit-slug>.png` (also uploaded as a build artifact).

Requires an `OPENAI_API_KEY` repo secret (Settings → Secrets and variables →
Actions). You can also render on demand from the Actions tab via *Run workflow*,
optionally naming a single kit slug and a quality level.
