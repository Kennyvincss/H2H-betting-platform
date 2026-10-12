# THE LAST COUNTDOWN: A TRUE Finance Original (1:41)

`the_last_countdown.mp4` is 1920×1080, 24 fps, 100.7 s, in 2.39:1 letterbox. It is a cinematic animatic: rim-lit silhouetted characters whose jaws move with their own voices, synthetic voices, an original score, and real TRUE branding and graphics. It is not live-action footage.

## What the film explains (Scene 4), all from true.foundation
| Question (Marcus) | Answer (Elena), as published by TRUE Foundation |
|---|---|
| What is $TRUE? | The utility and access token of the TRUE ecosystem, issued by TRUE Foundation on Solana. TRUE AI builds and runs the TRUE DEX, which is already live with over $1 billion traded (figures as at 8 Sep 2026, unaudited, per the site). |
| What is it used for? | Pay trading fees in $TRUE for up to 50% off; AI credits for TRUE AI requests; a higher copy-trading leader share for larger holdings; boosted referral payouts. VIP levels, burns, staking and vaults follow as each ships (**planned utility**, may change). |
| Why does the TGE matter? | 15 October 2026, 18:00 CET: token generation, and $TRUE opens for trading on the TRUE DEX. After listing, fee payment in $TRUE and VIP levels switch on. The contract address comes from official channels only. |

## Sources and graphics
- **true.foundation** (TRUE Foundation, the issuer): home, About, Tokenomics and Manifest pages. The film shows its own graphics on the display wall: the facts card, venue stats, utility cards, fee-discount panel and listing timeline (`tf/`). The listing date and time come from here.
- **truefinance.ai**: the official TRUE Finance logo (SVG lockup), the "Trade like you have a team." social image, and product-panel captures (`assets/`, `crops/`).

Deliberately left out: the token-sale price multiple shown on the Tokenomics page, revenue and profit figures, and any price, return or listing-performance claims. The end card carries the site's own caveats: planned utility may change; contract address on official channels only; not investment advice; not a guarantee of any return; not available in the US, UAE or sanctioned jurisdictions.

## Cast and voices (Piper TTS)
- **Marcus**: en-us-ryan-high
- **Elena**: en-us-libritts-high, speaker 250
- **Colleague**: en-gb-alan-low, phone EQ
- **Narrator**: en-us-libritts-high, speaker 800

"$TRUE", "TGE" and "VIP" are spelled in the voice script so they are pronounced correctly; subtitles show the proper spelling.

## Timeline
| Scene | Time (s) |
|---|---|
| 1 · The Warning | 0–8.9 |
| 2 · The Discovery | 8.9–22.1 |
| 3 · The Race Against Time | 22.1–32.5 |
| 4 · The Revelation: what / what for / why the TGE | 32.5–83.9 |
| 5 · The Countdown | 83.9–91.9 |
| 6 · The Final Reveal | 91.9–100.7 |

The scene 5 clock starts from the value shown on true.foundation's listing countdown when the site was captured and ticks in real time. It is a story device, not a live countdown.

## Rebuild
```bash
mkdir -p vo && python3 vo.py && python3 layout.py && python3 voice_fx.py
python3 -c "import json;open('vo/data.js','w').write('window.TL='+open('vo/timeline.json').read()+';window.ENV='+open('vo/env.json').read()+';')"
python3 score.py && ffmpeg -i mix_raw.wav -af loudnorm=I=-15:TP=-1.5:LRA=14 -ar 48000 mix.wav
mkdir frames && node render.js frames 24 0 100.69
ffmpeg -framerate 24 -i frames/f_%05d.jpg -i mix.wav -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac the_last_countdown.mp4
```
