# ClipRally Outro: "One Clip. Everywhere."

A stand-alone 5.000-second outro (300 frames at 60 fps). It opens on black, a clip gets cut out and clipped, multiplies into every kind of moment, and the ClipRally mascot punches out of the vortex.

| File | Use |
|---|---|
| `cliprally_outro_16x9.mp4` / `cliprally_outro_9x16.mp4` | **The outro**, ready to append to any clip. |
| `apply_outro.sh` | `./apply_outro.sh clip.mp4 out.mp4`: joins the matching outro (16:9 or 9:16, picked from the clip's shape) to the clip at the clip's size and frame rate. Takes seconds; no rendering. |
| `cliprally_logo.jpg` | The official ClipRally logo (mascot badge), used as supplied: shown inside its own circle at its native proportions, never stretched or redrawn. |
| `cliprally_outro_audio.wav` | Audio signature, 48 kHz stereo, about −14.6 LUFS, −1.8 dBTP. |
| `outro3.html`, `render.js`, `sound3.py`, `thumbs.html`, `thumbs/`, `hero.png` | Sources: the animation, frame renderer, audio, and the illustrated moments. |

## Timeline
| Time | Picture | Sound |
|---|---|---|
| 0.00 | Black | — |
| 0.00–0.30 | A red cut slices across the dark and splits open; a clip card ("NO WAY") punches through with its progress bar running out | Slicing swish, landing thump |
| 0.18–0.36 | A "✂️ CLIPPED" sticker slams onto the card's corner | Scissor snip + punch |
| 0.38–1.00 | One clip becomes many: copies fan out in 3D and flip, one by one, to other moments (reactions, gaming plays, screaming streamers, crowds) | Cards dealt out |
| 1.00–2.18 | The cards spin into a vortex; the camera dives, speeding up | Accelerating fly-by whooshes |
| 2.18–2.42 | Everything is pulled into the centre | Suction swell |
| 2.32–2.74 | The mascot logo punches out toward the camera; shockwave and red crystals | Deep impact |
| 2.82–3.24 | A light sweep crosses the logo | Shimmer |
| 2.92–3.30 | "CLIPPED ON CLIPRALLY" rises in | Ticks |
| 3.20–4.50 | Ripples spread across a network of nodes | Swells |
| 4.48–4.80 | Final beat: the mascot punches once more | Two-tone digital finish |
| 5.00 | Hard cut | — |

## Placement
- **16:9**: the logo spans x 760–1160 and the text x 733–1187, inside the 9:16 centre-crop column (x 656–1264).
- **9:16**: native layout, with a 600 px logo and larger text.
- **Logo resolution**: the logo source is 400×400 px, so it is pixel-for-pixel in 16:9 and scaled 1.5× in 9:16. A larger master file would make the vertical version sharper.

## Rebuild
```bash
python3 sound3.py                               # sig3.wav
mkdir f && node render.js f 60 0 -              # 16:9 frames (use 1 for 9:16)
ffmpeg -framerate 60 -i f/f_%04d.png -i sig3.wav -c:v libx264 -crf 16 -pix_fmt yuv420p -c:a aac -t 5 cliprally_outro_16x9.mp4
```
