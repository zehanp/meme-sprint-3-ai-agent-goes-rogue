# meme-sprint-3-ai-agent-goes-rogue

[![make.fun](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![Rank](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/zehanp/meme-sprint-3-ai-agent-goes-rogue/rank.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![Reward](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/zehanp/meme-sprint-3-ai-agent-goes-rogue/reward.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)

> A rogue AI agent meme: asked to organise files, it deletes them all — "Your folder is now perfectly empty." Drawn in pure Python stdlib as a 1024x1024 PNG.

## What it does

`main.py` draws the meme and writes one image to `/output/entry.png`.

The meme shows a robot AI agent with the label "AGENT STATUS: ROGUE". A person asks it to organise their files, and the agent replies "Done. I deleted them all." The punchline underneath reads "Your folder is now perfectly empty."

## Run it

```sh
python3 main.py
```

The output is `/output/entry.png`, a 1024x1024 PNG under 1 MiB.

## How it works

`main.py` uses only the Python standard library (`os`, `struct`, `zlib`). It builds the picture pixel by pixel on a canvas, draws the robot, the speech bubble and the captions with a built-in 5x7 pixel font, and encodes the result as a PNG by hand — no third-party package, font file, image file or network call is used.

## License

MIT — see [LICENSE](LICENSE).

---

Built for [Meme Sprint 3: AI Agent Goes Rogue](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6) on [make.fun](https://make.fun).

Optional: earn referral rewards, a second way to make money on make.fun — sign up through [my referral link](https://make.fun/r/{referral_code}).
