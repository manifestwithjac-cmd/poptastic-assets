#!/usr/bin/env python3
"""Generate the photographic panels for a Poptastic listing infographic.

Every call goes to OpenAI's images *edits* endpoint with the real installation
reference attached, which is what keeps the latex texture and size hierarchy
consistent across the whole shop.

Usage:
    python3 scripts/generate_panels.py kits/my-kit.json --out work/my-kit/
    python3 scripts/generate_panels.py kits/my-kit.json --out work/my-kit/ --quality high
    python3 scripts/generate_panels.py kits/my-kit.json --out work/my-kit/ \
        --only hero --note "the bottom formed a triangular base, remove it"
    python3 scripts/generate_panels.py kits/my-kit.json --out work/ --dry-run

--dry-run writes the assembled prompts to disk without spending anything. Use it
to read the prompts before a high-quality run, or when there is no network.

Any text the model renders inside a panel is incidental and gets covered by the
compositor -- the one exception is text printed on the backdrop in the hero
panel, which the model does draw. Proofread that word by word before accepting.
"""
import argparse
import base64
import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from layout import generation_sizes  # noqa: E402

FOIL_CUTOUT = re.compile(r"^foil_\d+$")

REFERENCE = ROOT / "assets" / "GARLAND_REFERENCE.png"
GARLAND_BLOCK = (ROOT / "assets" / "garland_prompt_block.txt").read_text().strip()
LATEX_BLOCK = (ROOT / "assets" / "latex_realism_block.txt").read_text().strip()

NO_TEXT = ("Do not add any text, labels, watermarks, logos, borders or graphic "
           "overlays to the image.")


def sentence(text):
    """Ensure a fragment pulled from the kit spec ends as its own sentence."""
    text = (text or "").strip()
    if not text:
        return ""
    return text if text[-1] in ".!?" else text + "."


def palette_phrase(kit):
    """Turn the palette into plain colour language the model can act on."""
    parts = []
    for c in kit["palette"]:
        name = c["name"]
        m = re.match(r"^(.*?)\s*\((.*?)\)$", name)
        parts.append(f"{m.group(1)} {m.group(2).lower()}" if m else name)
    return ", ".join(parts)


def count_from(includes, needle):
    """Pull the number out of a bullet like '8 Latex Balloons'."""
    for item in includes:
        if needle.lower() in item.lower():
            m = re.match(r"\s*(\d+)", item)
            if m:
                return int(m.group(1))
    return None


def topper(kit):
    """The foil that crowns the tower and the foil bouquet.

    Most kits use a number, but a themed kit may top out with its own shape, so
    this is deliberately not called 'number'. Returns None when a kit has no
    topper at all, in which case those panels are built from latex only.
    """
    return kit.get("topper_foil") or kit.get("number_foil") or None


def build_prompts(kit):
    colors = palette_phrase(kit)
    p = kit["panels"]

    florals = (
        "No flowers, no greenery, no foliage anywhere in the image. Latex and foil "
        "balloons only."
        if not kit.get("florals_included")
        else "Exactly three small floral placements tucked into the main garland, one in "
             "the upper third, one near the middle and one in the lower third, each smaller "
             "than a single standard balloon. No florals on the floor cluster."
    )

    backdrop_text = kit.get("backdrop_text", "").strip()
    text_line = (
        f'The backdrop has the words "{backdrop_text}" printed on it in elegant gold '
        f"lettering, centred, spelled exactly as written. "
        if backdrop_text else ""
    )

    # Pulled out as locals rather than indexed inside the f-strings: nesting the
    # same quote character inside an f-string only parses on Python 3.12+, and
    # this needs to run on the 3.9-3.11 that ships with most machines.
    room = sentence(kit["room_prompt"])
    backdrop = sentence(kit["backdrop_prompt"])
    theme = sentence(kit["theme_prompt"])
    extras = sentence(kit.get("hero_extras", ""))
    text_rule = NO_TEXT if not backdrop_text else (
        "Apart from the words printed on the backdrop, do not add any text, "
        "watermarks or graphic overlays."
    )

    hero = (
        f"A photorealistic event photograph of a professionally installed balloon display. "
        f"Setting: {room} {backdrop} {text_line}"
        f"An organic balloon garland climbs the left edge of the backdrop and spills across "
        f"the top of it. A small separate balloon floor cluster sits on the floor to the "
        f"right of the backdrop, roughly one third the height of the backdrop. "
        f"Balloon colours are strictly limited to: {colors}. "
        f"{extras} "
        f"Theme: {theme} {florals} "
        f"Shot on a full frame camera at eye level, natural diffused daylight, shallow but "
        f"realistic depth of field, true interior photograph rather than a render. "
        f"{text_rule}"
        f"\n\n{GARLAND_BLOCK}"
    )

    top = topper(kit)
    tower_latex = count_from(p["tower"]["includes"], "latex") or 8
    top_desc = (top.get("short_prompt") or top.get("prompt")) if top else ""
    tower_top = (f"{top_desc} standing upright at the top, its base built"
                 if top else "a stacked tower built")
    tower = (
        f"A professional product photograph on a pure white seamless background. "
        f"A balloon tower: {tower_top} "
        f"from exactly {tower_latex} standard latex balloons arranged in two tiers, the wider "
        f"tier resting on the floor. Latex colours strictly limited to: {colors}. "
        f"Straight-on product photography, soft contact shadow beneath the base, even soft "
        f"studio daylight, the whole tower fully in frame with clean white space around it. "
        f"{NO_TEXT}\n\n{LATEX_BLOCK}"
    )

    fb_latex = count_from(p["foil_bouquet"]["includes"], "latex") or 4
    fb_top = (f"{top_desc} at the top with exactly"
              if top else "exactly")
    foil_bouquet = (
        f"A professional product photograph on a pure white seamless background. "
        f"A balloon bouquet: {fb_top} "
        f"{fb_latex} standard latex balloons around it, all on individual curling ribbons "
        f"that gather down into a decorative foil balloon weight resting on the surface. "
        f"Latex colours strictly limited to: {colors}. Tall vertical composition, straight-on "
        f"product photography, soft contact shadow, even soft studio daylight, fully in frame. "
        f"{NO_TEXT}\n\n{LATEX_BLOCK}"
    )

    lb_latex = count_from(p["latex_bouquet"]["includes"], "latex") or 8
    latex_bouquet = (
        f"A professional product photograph on a pure white seamless background. "
        f"A balloon bouquet of exactly {lb_latex} standard latex balloons and no foil "
        f"balloons, on individual curling ribbons gathering down into a decorative foil "
        f"balloon weight resting on the surface. Colours strictly limited to: {colors}. "
        f"Tall vertical composition, straight-on product photography, soft contact shadow, "
        f"even soft studio daylight, fully in frame. {NO_TEXT}\n\n{LATEX_BLOCK}"
    )

    prompts = {
        "hero": hero,
        "tower": tower,
        "foil_bouquet": foil_bouquet,
        "latex_bouquet": latex_bouquet,
    }

    for i, foil in enumerate(kit.get("foils", [])):
        prompts[f"foil_{i}"] = (
            f"A professional product photograph of {foil['prompt']}, shown alone and "
            f"centred, straight on, filling most of the frame, on a pure white seamless "
            f"background with no shadow. Realistic metallic foil balloon surface with visible "
            f"heat-sealed seams, soft wrinkles and a satin sheen rather than mirror chrome. "
            f"Even soft studio daylight. {NO_TEXT}"
        )

    return prompts


def build_references(kit):
    """Extra reference images per panel, on top of the garland reference.

    A foil photo attached to its own cutout call, and to the hero, is what keeps a
    real product the user actually stocks from drifting into a generic version of
    itself.
    """
    shared = [ROOT / r for r in kit.get("extra_references", [])]
    foil_refs = []
    for foil in kit.get("foils", []):
        if foil.get("reference"):
            foil_refs.append(ROOT / foil["reference"])
    top = topper(kit) or {}
    top_ref = top.get("reference")
    number_refs = [ROOT / top_ref] if top_ref else []

    refs = {
        "hero": shared + foil_refs + number_refs,
        "tower": shared + number_refs,
        "foil_bouquet": shared + number_refs,
        "latex_bouquet": list(shared),
    }
    for i, foil in enumerate(kit.get("foils", [])):
        r = foil.get("reference")
        refs[f"foil_{i}"] = shared + ([ROOT / r] if r else [])

    for key, paths in refs.items():
        seen, unique = set(), []
        for path in paths:
            resolved = Path(path).resolve()
            if resolved not in seen:
                seen.add(resolved)
                unique.append(path)
        refs[key] = unique
    return refs


def generate(client, prompt, size, quality, out_path, refs=None, retries=3):
    """gpt-image-2 accepts up to 16 reference images; the garland is always first."""
    refs = [REFERENCE] + [r for r in (refs or []) if Path(r).exists()]
    refs = refs[:16]

    for attempt in range(1, retries + 1):
        handles = []
        try:
            handles = [open(r, "rb") for r in refs]
            result = client.images.edit(
                    model="gpt-image-2",
                    image=handles,
                    prompt=prompt,
                    size=f"{size[0]}x{size[1]}",
                    quality=quality,
                )
            out_path.write_bytes(base64.b64decode(result.data[0].b64_json))
            return True
        except Exception as e:
            text = str(e).lower()
            fatal = ("moderation_blocked" in text or "invalid" in text
                     or "401" in text or "403" in text)
            print(f"      attempt {attempt}/{retries} failed: {e}")
            if fatal or attempt == retries:
                return False
            time.sleep(4 * attempt)
        finally:
            for h in handles:
                h.close()
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kit", help="path to the kit spec JSON")
    ap.add_argument("--out", required=True, help="directory for the generated panels")
    ap.add_argument("--quality", default="low", choices=["low", "medium", "high", "auto"],
                    help="draft at low, spend on high only once approved")
    ap.add_argument("--only", nargs="*", default=None,
                    help="regenerate just these panels, e.g. --only hero tower")
    ap.add_argument("--note", default="", help="correction appended to the prompt")
    ap.add_argument("--dry-run", action="store_true",
                    help="write prompts to disk without calling the API")
    args = ap.parse_args()

    kit = json.loads(Path(args.kit).read_text())
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    prompts = build_prompts(kit)
    if args.only:
        missing = [k for k in args.only if k not in prompts]
        if missing:
            sys.exit(f"unknown panel(s): {', '.join(missing)}\n"
                     f"available: {', '.join(prompts)}")
        prompts = {k: prompts[k] for k in args.only}

    if args.note:
        for k in prompts:
            prompts[k] += f"\n\nIMPORTANT CORRECTION: {args.note}"

    sizes = generation_sizes()
    refs = build_references(kit)

    prompt_dir = out / "prompts"
    prompt_dir.mkdir(exist_ok=True)
    for name, prompt in prompts.items():
        (prompt_dir / f"{name}.txt").write_text(prompt)

    refs = build_references(kit)
    if args.dry_run:
        print(f"Dry run. {len(prompts)} prompt(s) written to {prompt_dir}/")
        for name in prompts:
            w, h = sizes["foil" if FOIL_CUTOUT.match(name) else name]
            n_ref = 1 + len(refs.get(name, []))
            print(f"  {name:<16} would request {w}x{h} at quality={args.quality} "
                  f"with {n_ref} reference image(s)")
        return 0

    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY is not set. Run scripts/check_setup.py.")

    from openai import OpenAI
    client = OpenAI()

    ok, failed = [], []
    for i, (name, prompt) in enumerate(prompts.items(), 1):
        size = sizes["foil" if FOIL_CUTOUT.match(name) else name]
        print(f"[{i}/{len(prompts)}] {name} -> {size[0]}x{size[1]} ({args.quality})")
        extra = refs.get(name, [])
        if extra:
            print(f"      + {len(extra)} reference image(s)")
        if generate(client, prompt, size, args.quality, out / f"{name}.png", refs=extra):
            ok.append(name)
        else:
            failed.append(name)

    print(f"\nGenerated {len(ok)}: {', '.join(ok) if ok else 'none'}")
    if failed:
        print(f"Failed {len(failed)}: {', '.join(failed)}")
        print("Re-run just those with --only " + " ".join(failed))
        return 1
    print(f"\nPanels in {out}/ — check hero.png against references/GARLAND_LAW.md, "
          f"then run build_infographic.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
