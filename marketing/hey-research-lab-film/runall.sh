#!/bin/bash
cd "$(dirname "$0")"
E=334.93; N=4
for k in 0 1 2 3; do
  a=$(python3 -c "print(round($E*$k/$N*30)/30)"); b=$(python3 -c "print(round($E*($k+1)/$N*30)/30)")
  node render.js frames 30 $a $b > render_$k.log 2>&1 &
done
wait; echo done
