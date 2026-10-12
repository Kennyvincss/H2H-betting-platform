# ClipRally Outro

A stand-alone 5.000-second outro (300 frames at 60 fps). It starts on black, a red energy vortex builds, and the ClipRally mascot punches out of it.

| File | Use |
|---|---|
| `cliprally_outro_16x9.mp4` / `cliprally_outro_9x16.mp4` | **The outro**, ready to append to any clip. |
| `apply_outro.sh` | `./apply_outro.sh clip.mp4 out.mp4`: joins the matching outro (picked from the clip's shape) to the clip at the clip's size and frame rate. Takes seconds. |
| `cliprally_logo.jpg` | The official ClipRally logo (mascot badge), used as supplied: shown inside its own circle at native proportions, never stretched or redrawn. |
| `cliprally_outro_audio.wav` | Audio signature, 48 kHz stereo, −15.3 LUFS, −1.5 dBTP. |
| `outro4.html`, `render.js`, `sound4.py` | Sources: the animation, frame renderer and audio. |

## Timeline
| Time | Picture | Sound |
|---|---|---|
| 0.00 | Black | — |
| 0.05–0.50 | A faint red ember glows in the centre | Low pulse |
| 0.20–1.36 | A red energy vortex builds: spiral arms of light and particles streaming inward, speeding up; speed lines | Rising energy, swirling whooshes |
| 1.36–1.62 | Everything is sucked into the centre | Suction swell |
| 1.52–1.94 | The mascot logo punches out toward the camera (overshoot and settle); shockwave and red crystals | Deep impact |
| 2.02–2.44 | A light sweep crosses the logo | Shimmer |
| 2.12–2.50 | "CLIPPED ON CLIPRALLY" rises in | Ticks |
| 2.37–4.50 | Ripples spread across a network of nodes; drifting embers; the logo glow pulses | Swells |
| 4.48–4.80 | Final beat: the mascot punches once more | Two-tone digital finish |
| 5.00 | Hard cut | — |

## Placement
- **16:9**: the logo spans x 760–1160 and the text x 733–1187, inside the 9:16 centre-crop column (x 656–1264).
- **9:16**: native layout, with a 600 px logo and larger text.
- **Logo resolution**: the logo source is 400×400 px, so it is pixel-for-pixel in 16:9 and scaled 1.5× in 9:16.

## Rebuild
```bash
python3 sound4.py && ffmpeg -i sig4.wav -af loudnorm=I=-15:TP=-1.5 -ar 48000 sig4n.wav
mkdir f && node render.js f 60 0 -              # 16:9 frames (use 1 for 9:16)
ffmpeg -framerate 60 -i f/f_%04d.png -i sig4n.wav -c:v libx264 -crf 16 -pix_fmt yuv420p -c:a aac -t 5 cliprally_outro_16x9.mp4
```
