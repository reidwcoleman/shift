#!/bin/bash
# graburl.sh NAME URL — fetch a Gemini full-size image URL straight into photos/gem/NAME.png
set -e
tmp=$(mktemp /tmp/gemXXXX.jpg)
code=$(curl -s -L -o "$tmp" -w "%{http_code}" "$2")
[ "$code" != "200" ] && { echo "http $code"; rm -f "$tmp"; exit 1; }
/Users/reidcoleman/Shift/.venv/bin/python -c "
from PIL import Image
im=Image.open('$tmp'); print('$1', im.size); im.convert('RGB').save('/Users/reidcoleman/Shift/photos/gem/$1.png')"
rm -f "$tmp"
