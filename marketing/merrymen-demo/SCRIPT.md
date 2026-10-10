# Merry Men AI — Cinematic Product Demo (60s)

`merrymen_demo.mp4` is a 1920×1080, 24 fps, 60-second animatic cut with an original synthesized score.
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
| Characters | Silhouette + on-screen dialogue in the animatic; cast actors for the final film |

Script changes from the brief, so no feature is invented: Merrymen is an autonomous
trading agent that works inside spending limits you sign and the blockchain enforces. It is not a
market-research chatbot, so the "understand the market" beats show the live agent board,
asking why an agent did or didn't trade, and the wall refusing trades.

## Shot list and dialogue

| Time | Picture | Dialogue |
|---|---|---|
| 0–5 | WIDE. Dark room, five monitors of jittering charts, trader from behind. Phone buzzes. Super: SHERWOOD · 02:47 AM | MARCUS (phone): "Tell me you've figured out what's happening." |
| 5–8.3 | CU monitors, handheld shake | TRADER: "Five screens. Three sources, all saying different things. The market's moving faster than I can keep up." |
| 8.3–10.7 | CU phone, Marcus on call | MARCUS: "Then stop doing it the hard way." · TRADER: "What other way is there?" |
| 10.7–12 | Black. Merrymen mark glows | MARCUS: "…Merrymen." |
| 12–16 | Push in on monitor: merrymen.si hero "Your agent. Your rules." | TRADER: "This is the one you keep telling me about?" · MARCUS: "Yes. Let me show you what it does." |
| 16–22 | Pan the 3 steps, highlighting each: You set the wall → It proposes → The chain decides | MARCUS: "You sign the limits. The agent proposes a trade. The chain checks it against what you signed." · TRADER: "Hold on. It trades for me — inside my rules?" · MARCUS: "That's the idea. Put it to work." |
| 22–25.4 | Push to live agent board | TRADER: "Alright. Let's see what these agents are actually doing." |
| 25.4–31 | CU board, shogun row highlighted, tag REAL DATA | TRADER: "Four hundred fifty-eight refused?" · MARCUS: "Every trade outside the caps gets turned back — and it's shown as loudly as a win." |
| 31–34.4 | AI assistant (Merrymen MCP connector): typing "Why hasn't my agent traded?" | TRADER: "And if it sits still, I can just ask it why?" |
| 34.4–37.1 | Permission row: "What it decided and why, what it refused, and why it has not traded." | MARCUS: "Exactly. But don't just read the answer. Understand it, then decide what you do." |
| 37.1–42 | Telegram commands: `/why`, `/cap` (only tightens), `/kill` | TRADER: "And I can steer it from Telegram, too?" · MARCUS: "Yes. That's what I wanted you to see." · TRADER: "Now I see why you kept recommending this." |
| 42–44.6 | Market crash, red flash, alarm (simulated) | — |
| 44.6–51.4 | Phone app: PEPE and TSLA refused rows highlighted red | TRADER: "A few minutes ago, I was completely lost." · MARCUS: "And now?" · TRADER: "Now I know what I'm looking at. I still make the call — it just can't break the rules I signed." |
| 51.4–53 | "It can never move funds, see keys, sign transactions, turn on live trading or loosen your signed limits." | — |
| 53–55.6 | Laptop closes | MARCUS: "So… was it worth trying?" · TRADER: "You should've shown me this a long time ago." |
| 55.6–60 | Logo reveal: MERRY MEN AI / Discover what you can do with AI. / merrymen.si · start on paper / risk line | — |

## Rebuild

```bash
python3 audio.py                              # writes score.wav
mkdir frames && node render.js frames 24 0 60 # 1440 JPEG frames of film.html
ffmpeg -framerate 24 -i frames/f_%05d.jpg -i score.wav -c:v libx264 -crf 20 \
  -pix_fmt yuv420p -c:a aac -b:a 192k -shortest merrymen_demo.mp4
```

`render.js` expects Playwright (`require` path points at the global install; adjust if needed).
