# THE LAST COUNTDOWN: A TRUE Finance Original (60 s)

`the_last_countdown.mp4` is 1920×1080, 24 fps, exactly 60.0 s, in 2.39:1 letterbox. It is a cinematic animatic: silhouetted characters whose jaws move with their voices, synthetic voices, an original score, and real TRUE Finance branding and interface captures. It is not live-action footage.

## What comes from truefinance.ai
| Element | Source |
|---|---|
| TRUE Finance logo (lockup) | Official SVG symbol `true-finance-lockup` from the site's own markup |
| "Trade like you have a team. / Research. Trade. Automate." billboard | Official social image `assets/og/og-home.png` |
| Tablet and screen-wall interface | Captures of truefinance.ai product pages (features grid; perpetual futures BTC-PERP panel; trading agents, swap, MCP and copy trading panels). The site labels these panels "Illustrative walkthrough · no live data or orders". |
| Colours | Site stylesheet: background `#0e0d16`, violet `#9b87ff` / `#6e56cf`, mint `#4ade87` |
| Platform description in dialogue | Matches the site: "Research, trade and automate in one workspace"; AI research, wallet-based trading, agents and copy trading |

**$TRUE TGE, 15 October 2026**: per the client, this date was announced on TRUE Finance's official X account. It does **not** appear on truefinance.ai, and no web source confirmed it, as of 12 Oct 2026. The end card says so in small print, together with "Not financial advice; crypto assets carry high risk." The film makes no claims about price, returns, listings or token utility.

## Cast and voices (Piper TTS, open models)
- **Marcus**: en-us-ryan-high
- **Elena**: en-us-libritts-high, speaker 250
- **Colleague**: en-gb-alan-low, phone EQ
- **Narrator**: en-us-libritts-high, speaker 800, hall reverb

Mouths are animated from each line's own loudness envelope. Characters are rim-lit profile silhouettes with consistent shapes, hair and clothes in every scene.

## Script changes for length
The scripted dialogue ran about 53 s of speech, which cannot fit 60 s alongside the required 2 s of black and the title hold. Delivery is about 8% faster, and four lines are lightly shortened with the same meaning. "TRUE TGE" is spoken as "True T-G-E" and subtitled "$TRUE TGE".

## Timeline
| Scene | Time (s) |
|---|---|
| 1 · The Warning | 0.0–8.8 |
| 2 · The Discovery | 8.8–21.4 |
| 3 · The Race Against Time | 21.4–31.8 (billboard silence at 30.7) |
| 4 · The Revelation | 31.8–44.3 |
| 5 · The Countdown | 44.3–52.5 |
| 6 · The Final Reveal | 52.5–60.0 (black and silence 52.5–54.5, pulse, logo, narrator at 55.2, title, impact at 57.9, fade) |

The T-minus clock in scene 5 is a story device: it ticks in real time from a fixed value and is not a live countdown.

## Rebuild
Requires ffmpeg, Node with Playwright, Python with numpy and `piper-tts`. Voices are the Piper v0.0.2 GitHub release models in `../voices/`.
```bash
mkdir -p vo && python3 vo.py && python3 layout.py && python3 voice_fx.py
python3 -c "import json;open('vo/data.js','w').write('window.TL='+open('vo/timeline.json').read()+';window.ENV='+open('vo/env.json').read()+';')"
python3 score.py && ffmpeg -i mix_raw.wav -af loudnorm=I=-15:TP=-1.5:LRA=14 -ar 48000 mix.wav
mkdir frames && node render.js frames 24 0 60
ffmpeg -framerate 24 -i frames/f_%05d.jpg -i mix.wav -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -t 60 the_last_countdown.mp4
```
