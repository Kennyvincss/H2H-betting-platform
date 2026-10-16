#!/bin/bash
cd "$(dirname "$0")"
for k in 0 1 2 3; do node render.js frames 30 $((k*15)) $((k*15+15)) > render_$k.log 2>&1 & done
wait; echo done
