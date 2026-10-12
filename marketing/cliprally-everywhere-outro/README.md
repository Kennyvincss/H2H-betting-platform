# ClipRally Outro: "One Clip. Everywhere."

A 5.000-second outro (300 frames at 60 fps). The clip ends, gets clipped, multiplies into every kind of moment, and the ClipRally mascot punches out of the vortex.

| File | Use |
|---|---|
| `cliprally_outro_16x9.mp4` / `cliprally_outro_9x16.mp4` | Finished previews over a stand-in clip frame (`sample_frame.png`). |
| `apply_outro.sh` | `./apply_outro.sh clip.mp4 out.mp4 [fps]`: renders the outro from the clip's real last frame and appends it at the clip's size and frame rate. Picks 16:9 or 9:16 from the clip's shape. Takes about 1m50s at 30 fps or about 3m45s at 60 fps on one core. |
| `cliprally_logo.jpg` | The official ClipRally logo (mascot badge), used as supplied: shown inside its own circle at its native proportions, never stretched or redrawn. |
| `cliprally_outro_audio.wav` | Audio signature, 48 kHz stereo, about −14.6 LUFS, −1.8 dBTP. |
| `outro3.html`, `render.js`, `sound3.py`, `thumbs.html`, `thumbs/` | Sources: the animation, frame renderer, audio, and the 12 illustrated moments. |

## Timeline
| Time | Picture | Sound |
|---|---|---|
| 0.00 | The clip's real last frame, unchanged, so the cut from the clip is invisible | — |
| 0.00–0.32 | The frame settles back into a player card; its red progress bar runs to the end | Pull-back swoosh |
| 0.16–0.36 | A "✂️ CLIPPED" sticker slams onto the card's corner | Scissor snip + punch |
| 0.38–1.00 | One clip becomes many: copies of the card fan out in 3D and flip, one by one, to other moments (reactions, gaming plays, screaming streamers, crowds) | Cards dealt out |
| 1.00–2.18 | The cards spin into a vortex; the camera dives, speeding up, with motion blur and speed lines | Accelerating fly-by whooshes |
| 2.18–2.42 | Everything is pulled into the centre | Suction swell |
| 2.32–2.74 | The mascot logo punches out toward the camera (overshoot and settle); shockwave and a burst of red crystals | Deep impact |
| 2.82–3.24 | A light sweep crosses the logo | Shimmer |
| 2.92–3.30 | "CLIPPED ON CLIPRALLY" letters rise in | Ticks |
| 3.20–4.50 | Ripples spread across a network of nodes that light up as each ripple passes | Swells |
| 4.48–4.80 | Final beat: the mascot punches once more, with a ring | Two-tone digital finish |
| 5.00 | Hard cut | — |

## Placement
- **16:9**: the logo spans x 760–1160 and the text x 733–1187, inside the 9:16 centre-crop column (x 656–1264).
- **9:16**: native layout, with a 600 px logo and larger text.
- **Logo resolution**: the logo source is 400×400 px, so it is pixel-for-pixel at 1080p landscape and scaled 1.5× in the vertical version. A larger master file of the mascot would make the vertical version sharper.
