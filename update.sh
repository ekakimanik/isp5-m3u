#!/data/data/com.termux/files/usr/bin/bash
cd "$(dirname "$0")" || exit 1
python generate.py || exit 1
git add playlist.m3u generate.py update.sh
git commit -m "update $(date +%F-%H:%M)" || echo "No changes"
git push -u origin HEAD && echo "Done! GitHub updated."
