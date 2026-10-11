# ClipRally Outro — "The clip ends. The hype doesn't."

A 5.000-second (300 frames at 60 fps) branded outro that plays after every ClipRally clip.

| File | Use |
|---|---|
| `cliprally_outro_overlay_16x9.webm` | **Production overlay**: VP9 with alpha, 1920×1080, with audio. Transparent during the impact so the clip's frozen last frame shows through. |
| `cliprally_outro_overlay_9x16.webm` | Same, native 1080×1920 for Shorts/TikTok/Reels. |
| `cliprally_outro_preview_16x9.mp4` / `_9x16.mp4` | Previews over a stand-in clip frame (`sample_frame.png`). |
| `cliprally_outro_audio.wav` | Audio signature alone (48 kHz stereo, about −17.5 LUFS, −1 dBTP). |
| `apply_outro.sh` | `./apply_outro.sh clip.mp4 out.mp4`: freezes the clip's last frame for 5 s, lays the overlay on top and appends the audio. Picks 16:9 or 9:16 by clip shape. |

## Timeline
- **0.0–1.5 Impact**: frozen frame, flash, three shockwave rings, light streaks, particle burst, RGB glitch bands; the dark brand environment takes over from 0.95 s.
- **1.5–3.0 Brand reveal**: the wordmark assembles from 20 fragments and snaps at 2.00 s (flash, ring, shake); "CLIPPED ON CLIPRALLY" wipes in at 2.12 s.
- **3.0–5.0 Signature**: logo settles with a pulsing red glow; "YOUR NEXT VIRAL MOMENT / STARTS HERE." appears at 3.12 s; three-note chime at 3.15 s; hard cut at 5.00 s.

## Brand
- **Logo**: the official cliprally.com wordmark, rendered exactly as the site does. "Clip" is `#ffffff` and "Rally" is `--cr-red #f13549`, in Inter ExtraBold (800) with −0.045em tracking. The fragment animation only slices copies of it; the settled logo is unaltered. The mascot icon is published only at 32×32 px, so it is not used.
- **Colors**: `--cr-bg #101011`, `--cr-red #f13549`, `--cr-red-2 #bb1b30`, `--cr-cyan #35c8e8`, `--cr-text #f5f3ee`.
- **9:16 safe area**: on the 16:9 version, every logo and text element stays within x 702–1218, inside the centre-crop column x 656–1264.

## Rebuild
```bash
python3 sound.py                                       # sig.wav
node render.js frames 60 0 1 -                         # 16:9 alpha frames (use 1 1 for 9:16)
ffmpeg -framerate 60 -i frames/f_%04d.png -i sig.wav -c:v libvpx-vp9 -pix_fmt yuva420p \
  -b:v 6M -auto-alt-ref 0 -c:a libopus -t 5 cliprally_outro_overlay_16x9.webm
# ProRes 4444 master for editors (~220 MB, not committed):
ffmpeg -framerate 60 -i frames/f_%04d.png -i sig.wav -c:v prores_ks -profile:v 4444 \
  -pix_fmt yuva444p10le -c:a pcm_s16le -t 5 cliprally_outro_overlay_16x9.mov
```
Preview mode: `node render.js frames 60 0 0 /abs/path/to/frame.png` renders over a given frame.
