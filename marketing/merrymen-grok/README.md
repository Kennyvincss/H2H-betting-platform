# Merrymen × Grok: 60-second feature demo

`merrymen_x_grok.mp4` is the video: 1920×1080, 30 fps, exactly 60 s, mastered to about −16 LUFS. It uses the same format as `../merrymen-demo`:

- **Cast:** Marcus (who is on the phone in the opening) and the trader, as voiced silhouette characters. Their jaws are synced to the voices.
- **Screens:** real captures of merrymen.si/grok, taken 16 Oct 2026. Lime highlights mark the part of each screen being discussed.
- **The one mock-up:** the laptop chat in the opening is illustrative and labelled as such on screen.

## What the video claims

Everything below is from merrymen.si/grok.

- Add Merrymen to Grok once, as a custom connector (`https://mcp.merrymen.dev/mcp`). No model API key is needed.
- Sign in and choose which Merryman and permissions Grok can see.
- "Set up a practice Merryman for me." Grok prepares the setup, and you review it and sign the limits in Merrymen.
- You can then ask Grok:
  - "What remains before my Merryman is running?"
  - "Why hasn't my agent traded?"
  - for your recent trades, with practice and live kept separate.
- The connector cannot sign wallet transactions or loosen your signed limits. You can disconnect at any time.

The end card also carries the page's own caveat: Merrymen has tested this on Grok web, and the Grok Bot setup is not yet verified.

## Rebuild

```
python3 vo.py && python3 layout.py && python3 voice_fx.py && python3 build_data.py
./runall.sh && python3 score.py
ffmpeg -i mix_raw.wav -af loudnorm=I=-15:TP=-1.5 mix.wav
ffmpeg -framerate 30 -i frames/f_%05d.jpg -i mix.wav -c:v libx264 -crf 24 -pix_fmt yuv420p -c:a aac out.mp4
```

`vo.py` needs the Piper voices in `../voices`.
