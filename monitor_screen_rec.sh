#!/bin/sh
until ~/Dropbox/screen_recorder/_2_take_screenshots.py; do
    echo "screen_recorder crashed with exit code $?.  Respawning.." >> ~/screenshots.err >&2
    sleep 10
done
