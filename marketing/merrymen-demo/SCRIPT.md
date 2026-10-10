# Merry Men AI — Cinematic Product Demo (60s)

`merrymen_demo.mp4` is a 1920×1080, 24 fps, 60-second animatic cut with voiced dialogue and an original synthesized score.
It doubles as the edit blueprint for a live-action shoot: every product insert below is a real
capture of merrymen.si (taken 10 Oct 2026); only the "actor" shots need to be filmed.

## What is real vs. dramatized

| Element | Status |
|---|---|
| Homepage, "how it works" steps, live agent board (shogun: 119 landed / 458 refused) | Real captures, live public data |
| Prompt "Why hasn't my agent traded?" | Real example prompt from merrymen.si/claude |
| "See your agent's decisions" permission row, "It can never move funds…" | Real text from merrymen.si/claude |
| Telegram commands (`/why`, `/cap`, `/kill`) | Real, from merrymen.si/docs |
| Phone app with "TSLA refused · past today's spending cap" | Real UI from merrymen.si/app — **demo build, generated numbers** (labeled on screen) |
| Room, monitors, market crash chart | Dramatization, labeled "simulated" |
| Characters | Silhouette, plus synthetic voices (Piper TTS: Ryan for the trader, LibriTTS speaker 400 for Marcus) with matching subtitles. Recast with actors for the final film |

Script changes from the brief, so no feature is invented: Merrymen is an autonomous
trading agent that works inside spending limits you sign and the blockchain enforces. It is not a
market-research chatbot, so the "understand the market" beats show the live agent board,
asking why an agent did or didn't trade, and the wall refusing trades.

## Dialogue (voiced, final timing)

Marcus is on the phone in Scene 1 (phone EQ), then on speaker. The trader is in the room.

| Time (s) | Speaker | Line |
|---|---|---|
| 2.4–3.9 | MARCUS | Tell me you’ve figured out what’s happening. |
| 4.1–8.3 | TRADER | Five screens. Three sources, all saying different things. It’s moving faster than I can keep up. |
| 8.5–9.9 | MARCUS | Then stop doing it the hard way. |
| 10.2–11.1 | TRADER | What other way is there? |
| 11.5–12.1 | MARCUS | ... Merrymen. |
| 12.3–14.1 | TRADER | This is the one you keep telling me about? |
| 14.3–15.8 | MARCUS | Yes. Let me show you. |
| 16.1–19.2 | MARCUS | You sign the limits. It proposes. The chain enforces. |
| 19.4–21.6 | TRADER | Hold on. It trades for me — inside my rules? |
| 21.9–23.4 | MARCUS | That’s the idea. Put it to work. |
| 23.9–25.7 | TRADER | Alright. Let’s see what they’re actually doing. |
| 26.0–27.4 | TRADER | Four hundred fifty-eight refused? |
| 27.7–31.9 | MARCUS | Outside the caps, it’s refused — shown as loudly as a win. |
| 32.2–34.0 | TRADER | And if it sits still, I can ask it why? |
| 34.3–37.5 | MARCUS | Exactly. Don’t just read the answer. Understand it, then decide. |
| 37.8–39.3 | TRADER | And I can steer it from Telegram, too? |
| 39.6–41.4 | MARCUS | Yes. That’s what I wanted you to see. |
| 41.7–43.4 | TRADER | Now I see why you kept recommending this. |
| 45.9–48.0 | TRADER | A few minutes ago, I was completely lost. |
| 48.2–48.7 | MARCUS | And now? |
| 49.0–52.4 | TRADER | Now I know what I’m looking at. I make the call — it just can’t break my rules. |
| 53.3–54.5 | MARCUS | So. Worth trying? |
| 54.7–56.5 | TRADER | You should’ve shown me this a long time ago. |

## Picture

| Scene | Picture |
|---|---|
| 1 · Problem | Dark room, five monitors of jittering charts, trader from behind, phone buzzes (SHERWOOD · 02:47 AM) → handheld close-up of monitors → phone on call with Marcus → black, Merrymen mark glows |
| 2 · Product | Push in on merrymen.si hero "Your agent. Your rules." → the 3 steps highlighted in turn: You set the wall / It proposes / The chain decides |
| 3 · Live demo | Live agent board (shogun 119 landed / 458 refused, tagged REAL DATA) → "Why hasn't my agent traded?" typed into an AI assistant with the Merrymen connector → "See your agent's decisions" permission row → Telegram commands `/why`, `/cap`, `/kill` |
| 4 · Payoff | Simulated market crash and alarm → phone app with PEPE / TSLA refused rows (demo build) → "It can never move funds, see keys … or loosen your signed limits." |
| 5 · Brand | Laptop closes → MERRY MEN AI / Discover what you can do with AI. / merrymen.si · start on paper / risk line |

## Rebuild

Requires ffmpeg, Node with Playwright, Python with numpy, and `pip install piper-tts`.
Voices (not committed, ~200 MB) come from the Piper v0.0.2 GitHub release into `voices/`:
`voice-en-us-ryan-high.tar.gz` and `voice-en-us-libritts-high.tar.gz`.

```bash
mkdir -p vo && python3 vo.py   # synthesize each line from the LINES table in film.html
python3 layout.py              # trim, tempo, timing -> vo/layout.json, vo/warp.json (paste warp into film.html WARP)
python3 audio.py               # music + sound design -> music.wav
python3 mix.py                 # voice processing, ducking, mix -> score.wav
mkdir frames && node render.js frames 24 0 60
ffmpeg -framerate 24 -i frames/f_%05d.jpg -i score.wav -c:v libx264 -crf 20 \
  -pix_fmt yuv420p -c:a aac -b:a 192k -shortest merrymen_demo.mp4
```
