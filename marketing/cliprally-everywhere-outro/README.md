# ClipRally Outro: "One Clip. Everywhere."

A 5.000-second outro (300 frames at 60 fps) in which the clip's own last frame shatters into dozens of video clips, spins into a vortex, and collapses into the ClipRally logo.

| File | Use |
|---|---|
| `cliprally_everywhere_preview_16x9.mp4` / `_9x16.mp4` | Previews over a stand-in clip frame (`sample_frame.png`). |
| `apply_everywhere.sh` | `./apply_everywhere.sh clip.mp4 out.mp4 [fps]`: grabs the clip's real last frame, renders the outro with it, and appends it (with audio) at the clip's size and frame rate. Picks 16:9 or 9:16 from the clip's shape. |
| `cliprally_everywhere_audio.wav` | Audio signature, 48 kHz stereo, about −14.6 LUFS, −1.8 dBTP. |
| `outro2.html`, `render.js` | The animation (`outro2.html?v=0|1&frame=<image>`) and the frame renderer. |
| `thumbs.html`, `thumbs/` | The 12 illustrated "moments" the frame shatters into: reactions, gaming plays, screaming streamers, crowds. |
| `sound2.py` | Rebuilds the audio. |

## Timeline
| Time | Picture | Sound |
|---|---|---|
| 0.00–0.10 | The clip's last frame, frozen and untouched, so it follows on seamlessly | — |
| 0.10–0.40 | The glass cracks out from the impact point; camera shake | Glass crack, crackle, tinkles |
| 0.40–1.00 | 65 shards break away in 3D toward the camera; each turns into a video card | Shatter burst |
| 1.00–2.18 | The cards form a spinning helix tunnel; the camera dives, speeding up, with speed lines and motion blur | Accelerating fly-by whooshes over a rising tone |
| 2.18–2.42 | Everything is sucked into the centre | Reverse suction swell |
| 2.42–2.86 | Flash and shockwave; the logo assembles from 22 slices flying out of depth | Deep impact |
| 2.80–3.20 | A light sweep crosses the logo | Shimmer |
| 2.98–3.35 | "CLIPPED ON CLIPRALLY" letters rise in | Ticks |
| 3.20–5.00 | Three ripples spread out across a network of nodes that light up as each ripple passes | Soft swells |
| 4.50 | — | Two-tone digital finish |
| 5.00 | Hard cut | — |

## Brand rules
- **Logo**: the official cliprally.com wordmark, rendered exactly as the site does. "Clip" is #ffffff and "Rally" is #f13549, in Inter ExtraBold (800) with −0.045em tracking. The slices used in the assembly are clipped copies of it; from 2.86 s the settled logo is the unaltered wordmark. The 32×32 mascot favicon is too small to use.
- **Text**: exactly `CLIPPED ON CLIPRALLY`, with "CLIPRALLY" in the brand red.
- **9:16 safe area (16:9 version)**: the logo spans x 702–1218 and the text x 733–1187, both inside the centre-crop column x 656–1264. The vertical version uses larger type.

## Rendering cost
The shatter uses each clip's real last frame, so the outro is rendered per clip. That takes about 3–4 minutes on one CPU core at 60 fps here. Pass `30` as the fps to halve it, or render frame ranges in parallel; the code is deterministic, so frames can be split across workers.
