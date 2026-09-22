#!/bin/bash
# grab.sh NAME [DIR] — move the Gemini download from the last 3 minutes into DIR/NAME.png (default art/color/NAME_raw.png)
set -e
f=$(find ~/Downloads -maxdepth 1 \( -name "Gemini_Generated_Image_*" -o -name "[0-9]*.jpeg" \) -mmin -3 -print0 2>/dev/null | xargs -0 ls -t 2>/dev/null | head -1)
[ -z "$f" ] && { echo "no recent download"; exit 1; }
if [ -n "$2" ]; then out="/Users/reidcoleman/Shift/$2/$1.png"; else out="/Users/reidcoleman/Shift/art/color/$1_raw.png"; fi
~/Shift/.venv/bin/python -c "from PIL import Image; im=Image.open('$f'); print(im.size); im.convert('RGB').save('$out')"
rm -f "$f"; echo "$out"
