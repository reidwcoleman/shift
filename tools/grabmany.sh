#!/bin/bash
# grabmany.sh NAME1 NAME2 ... — assign the N most recent Gemini downloads (oldest first) to the names in order
n=$#
files=$(find ~/Downloads -maxdepth 1 \( -name "Gemini_Generated_Image_*" -o -name "[0-9]*.jpeg" \) -mmin -30 -print0 | xargs -0 ls -tr 2>/dev/null | tail -n $n)
cnt=$(echo "$files" | grep -c .)
[ "$cnt" -ne "$n" ] && { echo "expected $n downloads, found $cnt"; exit 1; }
i=0
echo "$files" | while read -r f; do
  i=$((i+1)); name=${!i}
  /Users/reidcoleman/Shift/.venv/bin/python -c "from PIL import Image; im=Image.open('$f'); print('$name', im.size); im.convert('RGB').save('/Users/reidcoleman/Shift/photos/gem/$name.png')"
  rm -f "$f"
done
