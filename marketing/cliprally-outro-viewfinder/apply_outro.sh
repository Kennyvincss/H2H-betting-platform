#!/usr/bin/env bash
# Append the ClipRally outro to a clip. The outro is a fixed 5 s file, so this is a quick
# re-encode/join: picks the 16:9 or 9:16 version from the clip's shape and matches its size and frame rate.
# Usage: ./apply_outro.sh input.mp4 output.mp4
set -euo pipefail
IN="$1"; OUT="$2"; DIR="$(cd "$(dirname "$0")" && pwd)"
read -r W H < <(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0:s=x "$IN" | tr x ' ')
CFPS=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$IN")
if (( H > W )); then OUTRO="$DIR/cliprally_outro_viewfinder_9x16.mp4"; else OUTRO="$DIR/cliprally_outro_viewfinder_16x9.mp4"; fi
if ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$IN" | grep -q .; then A="[0:a]aresample=48000,aformat=channel_layouts=stereo[ca]"; else
  A="anullsrc=r=48000:cl=stereo,atrim=0:$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")[ca]"; fi
ffmpeg -y -v error -i "$IN" -i "$OUTRO" -filter_complex \
 "[0:v]fps=$CFPS,setsar=1,format=yuv420p[cv];[1:v]scale=${W}:${H}:force_original_aspect_ratio=increase,crop=${W}:${H},fps=$CFPS,setsar=1,format=yuv420p[ov];\
  $A;[1:a]aresample=48000,aformat=channel_layouts=stereo[oa];[cv][ca][ov][oa]concat=n=2:v=1:a=1[v][a]" \
 -map "[v]" -map "[a]" -c:v libx264 -crf 18 -preset medium -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
echo "wrote $OUT"
