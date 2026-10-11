#!/usr/bin/env bash
# Append the ClipRally outro to a clip: the clip's last frame freezes for 5s under the
# transparent outro overlay, and the outro's audio signature plays after the clip's audio.
# Usage: ./apply_outro.sh input.mp4 output.mp4
set -euo pipefail
IN="$1"; OUT="$2"; DIR="$(cd "$(dirname "$0")" && pwd)"
read -r W H < <(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0:s=x "$IN" | tr x ' ')
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
if (( H > W )); then OV="$DIR/cliprally_outro_overlay_9x16.webm"; else OV="$DIR/cliprally_outro_overlay_16x9.webm"; fi
HAS_AUDIO=$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$IN" | head -1)
DMS=$(python3 -c "print(int(round($DUR*1000)))")
if [[ -n "$HAS_AUDIO" ]]; then
  AUD="[0:a]aresample=48000,apad=whole_dur=$(python3 -c "print($DUR+5)")[ca];[1:a]aresample=48000,adelay=${DMS}|${DMS}[oa];[ca][oa]amix=inputs=2:normalize=0:duration=first[a]"
else
  AUD="[1:a]aresample=48000,adelay=${DMS}|${DMS},apad=whole_dur=$(python3 -c "print($DUR+5)")[a]"
fi
ffmpeg -y -v error -i "$IN" -c:v libvpx-vp9 -i "$OV" -filter_complex \
 "[0:v]tpad=stop_mode=clone:stop_duration=5,setsar=1[base];\
  [1:v]scale=${W}:${H}:force_original_aspect_ratio=increase,crop=${W}:${H},setpts=PTS+${DUR}/TB[ov];\
  [base][ov]overlay=0:0:eof_action=pass:format=auto[v];$AUD" \
 -map "[v]" -map "[a]" -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k \
 -t "$(python3 -c "print($DUR+5)")" -movflags +faststart "$OUT"
echo "wrote $OUT"
