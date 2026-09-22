#!/bin/bash
# grabwait.sh NAME — wait up to 40 s for a fresh Gemini download, then grab it into photos/gem/NAME.png
for i in $(seq 1 20); do
  f=$(find ~/Downloads -maxdepth 1 \( -name "Gemini_Generated_Image_*" -o -name "[0-9]*.jpeg" \) -mmin -2 | head -1)
  [ -n "$f" ] && break; sleep 2
done
exec /Users/reidcoleman/Shift/tools/grab.sh "$1" photos/gem
