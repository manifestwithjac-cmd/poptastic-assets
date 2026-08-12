# OpenAI Images API — setup and parameters

This skill uses **OpenAI's `gpt-image-2`**, not Higgsfield and not Claude. Everything below is
the OpenAI Images API.

## One-time setup

1. **Get a key.** platform.openai.com → Settings → API keys → create a new secret key. It is
   shown once; save it immediately.
2. **Load billing.** Settings → Billing. The Images API is pay-as-you-go and separate from a
   ChatGPT Plus subscription — Plus does not include API credit.
3. **Complete API Organization Verification.** Settings → Organization → General. GPT Image
   models are gated behind it; without it every call fails with a model-access error. It uses
   a government ID check and can take a little time to clear.
4. **Set the key in the environment**, never in a file that gets committed:

```bash
export OPENAI_API_KEY="sk-..."
```

To persist it, add that line to `~/.zshrc` (Mac default shell) or `~/.bashrc`, then restart
the terminal. Verify with `python3 scripts/check_setup.py`.

5. **Install the SDK:** `pip install openai pillow`

## The call this skill makes

Reference images require the **edits** endpoint, not generations. `gpt-image-2` accepts up to
16 reference images and uses them as visual guidance for a new image rather than editing them
in place.

```python
result = client.images.edit(
    model="gpt-image-2",
    image=[open("assets/GARLAND_REFERENCE.png", "rb")],
    prompt=prompt,
    size="1312x1168",
    quality="high",
)
image_bytes = base64.b64decode(result.data[0].b64_json)
```

Equivalent curl, useful for debugging auth:

```bash
curl -X POST "https://api.openai.com/v1/images/edits" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F "model=gpt-image-2" \
  -F "image[]=@assets/GARLAND_REFERENCE.png" \
  -F "prompt=..." | jq -r '.data[0].b64_json' | base64 --decode > out.png
```

## Parameters that matter here

**`size`** — `gpt-image-2` accepts arbitrary resolutions within these constraints, which is why
panels can be generated at their exact final aspect ratio instead of being cropped:

- Both edges must be multiples of 16
- Longest edge ≤ 3840 px
- Long:short ratio ≤ 3:1
- Total pixels between 655,360 and 8,294,400

`scripts/generate_panels.py` snaps requested panel sizes to satisfy all four automatically.

**`quality`** — `low` / `medium` / `high` / `auto`. Always draft at `low`; it is roughly forty
times cheaper than `high` and composition problems are just as visible. Switch to `high` only
for the approved final.

**`input_fidelity`** — do not send it. `gpt-image-2` processes every reference at high fidelity
automatically and rejects the parameter.

**`background`** — `gpt-image-2` does not support transparent backgrounds. Product panels are
generated on pure white instead, and the layout uses white panel cards so they blend seamlessly.
No keying needed.

## Cost per image (approximate, USD)

| Quality | 1024×1024 |
|---|---|
| low | $0.006 |
| medium | $0.053 |
| high | $0.211 |

A full listing is roughly 4 panels plus one image per foil shape. A typical kit with three
foils is about 7 images: pennies as a low-quality draft, around $1.50 at high. Reference images
add input tokens on top, since they are always processed at high fidelity. Check the current
pricing page before quoting exact numbers to the user.

## Errors worth recognizing

| Symptom | Cause | Fix |
|---|---|---|
| 401 | key missing, wrong, or revoked | re-export `OPENAI_API_KEY` |
| 403 / model not found | organization not verified | complete API Organization Verification |
| 429 | rate limit or no credit | check billing balance; retry with backoff |
| `invalid size` | edge not a multiple of 16, or pixel count out of range | let the size-snapping helper handle it |
| `moderation_blocked` | prompt tripped a filter | reword; do not retry unchanged |
| Empty or garbled text in output | expected | text is drawn by the compositor, not the model — ignore any text the model renders |

Retry `429` and `5xx` with backoff. Do not auto-retry a `moderation_blocked` or an invalid
parameter — those need the request changed.

## Latency

Complex prompts can take up to two minutes per image. Generating seven panels serially is slow
enough to be worth warning the user about before starting a high-quality run.
