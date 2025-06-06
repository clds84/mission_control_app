#!/bin/bash
# /home/cristian/start_chromium.sh

export DISPLAY=:0

chromium-browser --ozone-platform=x11 --start-fullscreen --incognito --noerrdialogs --disable-session-crashed-bubble --disable-infobars --no-first-run --disable-translate --disable-features=TranslateUI --user-data-dir=/tmp/chromium-temp-profile http://headless4.local:8000
