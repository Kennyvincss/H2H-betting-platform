# Who's Actually Building? — a HEY Research Lab explainer (5:35)

`hey_research_lab_explainer.mp4`: 1920×1080, 30 fps, about 5 min 35 s, mastered to −15 LUFS. It was made for the HEY Research Lab contest thread.

Jade (a trader) asks the questions and Nico (a researcher) walks her through **real heyresearch.xyz screens**, captured on 12 Oct 2026. Highlights mark the part of each screen being discussed, and every on-screen figure is as captured.

## Chapters

1. What HEY Research Lab is: builder evidence vs price; every ship has a source; Fact / Derived / Unknown.
2. HEY Research Discovery: Explore, counts, and activity statuses (Shipping, Active, Quiet, Dormant, Resumed, Activity unknown).
3. Ships, Signals, Narratives and Pulse.
4. Build Momentum, Discovery Gap, Under the Radar ("Building, little attention") and Still Building. These are context, not buy signals.
5. Scan: "Is anyone building this?"
6. A real project page (Merrymen).
7. The Research Terminal:
   - research summary with receipts, timeline, ships & releases, the market chart with build events, on-chain activity and sources;
   - What changed, Compare, Research queue and Ask HEY;
   - the three ways in.
8. For builders and developers: claim / badge / embed, the public API, the SDK and MCP.
9. The $HEY token: launched on Pons, no presale, pays for research work, never buys a ranking.
10. How I'd use it, and why it matters on Robinhood Chain.

## Rebuild

```
python3 vo.py && python3 layout.py && python3 voice_fx.py && python3 build_data.py
./runall.sh
python3 score.py
ffmpeg -i mix_raw.wav -af loudnorm=I=-15:TP=-1.5 mix.wav
ffmpeg -framerate 30 -i frames/f_%05d.jpg -i mix.wav -c:v libx264 -crf 23 -pix_fmt yuv420p -c:a aac out.mp4
```

What the steps use:

- `vo.py` needs the Piper voices in `../voices`.
- `runall.sh` renders the frames in 4 parallel headless-Chromium processes.

Independent fan-made explainer; not affiliated with HEY Research Lab or Robinhood. Not investment advice.
