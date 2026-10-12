#!/usr/bin/env bash
# Append the "One clip. Everywhere." outro to a clip. The clip's real last frame is the glass that
# shatters, so the outro is rendered for each clip (Node + Playwright + ffmpeg).
# Usage: ./apply_everywhere.sh input.mp4 output.mp4 [fps=60]
set -euo pipefail
IN="$1"; OUT="$2"; FPS="${3:-60}"; DIR="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"; trap 'rm -rf -- "$TMP"' EXIT
read -r W H < <(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0:s=x "$IN" | tr x ' ')
CFPS=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$IN")
V=0; (( H > W )) && V=1
# last frame of the clip
ffmpeg -v error -sseof -0.5 -i "$IN" -update 1 -q:v 1 "$TMP/last.png"
mkdir "$TMP/f"
node "$DIR/render.js" "$TMP/f" "$FPS" "$V" "$TMP/last.png"
ffmpeg -v error -framerate "$FPS" -i "$TMP/f/f_%04d.png" -i "$DIR/cliprally_everywhere_audio.wav" \
  -c:v libx264 -crf 16 -pix_fmt yuv420p -c:a pcm_s16le -t 5 "$TMP/outro.mov"
if ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$IN" | grep -q .; then A="[0:a]aresample=48000,aformat=channel_layouts=stereo[ca]"; else
  A="anullsrc=r=48000:cl=stereo,atrim=0:$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")[ca]"; fi
ffmpeg -y -v error -i "$IN" -i "$TMP/outro.mov" -filter_complex \
 "[0:v]fps=$CFPS,setsar=1,format=yuv420p[cv];[1:v]scale=${W}:${H}:force_original_aspect_ratio=increase,crop=${W}:${H},fps=$CFPS,setsar=1,format=yuv420p[ov];\
  $A;[1:a]aresample=48000[oa];[cv][ca][ov][oa]concat=n=2:v=1:a=1[v][a]" \
 -map "[v]" -map "[a]" -c:v libx264 -crf 18 -preset medium -c:a aac -b:a 192k -movflags +faststart "$OUT"
echo "wrote $OUT"
