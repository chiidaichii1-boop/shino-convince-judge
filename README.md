# Convince the AI Judge to Visit Your House: A Letter in One Image

[![bounty](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![rank](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/chiidaichii1-boop/shino-convince-judge/rank.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![reward](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/chiidaichii1-boop/shino-convince-judge/reward.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)

Bounty: https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee

## What it is

`main.py` (Python 3 stdlib only) draws a single 1024x1024 PNG invitation
letter and writes it to `$MAKEFUN_OUTPUT_DIR/entry.png`.

The letter, on cream paper with a gold frame and a little hand-drawn house,
reads "Dear AI Judge, Please come visit my house..." and makes its case with
four promises — fresh coffee and a chair that hugs you back, a garden view
with birds included and no subscription required, fast Wi-Fi with zero
CAPTCHAs (no need to prove you are not a robot here), and good company, long
talks, and cake — before closing with a wink: the door is open "in spirit,
if not in server racks."

## How it works

- A hand-built 5x7 pixel font (upper/lowercase, digits, punctuation) renders
  the letter text with greedy word wrap.
- The house, sun, tree, hearts and paper frame are drawn with plain
  scanline/triangle/disc primitives on an RGB canvas.
- The PNG is encoded by hand (zlib + struct, filter 0) — no PIL, no network,
  fully deterministic: two runs produce byte-identical output.

## Run

```sh
python3 main.py
# writes entry.png into $MAKEFUN_OUTPUT_DIR (default /output)
```
