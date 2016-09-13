launchctl unload ~/Library/LaunchAgents/com.jessealdridge.screenshots.plist
launchctl load ~/Library/LaunchAgents/com.jessealdridge.screenshots.plist
launchctl list | grep jesse
sleep 1
tail -f ~/screenshots.log ~/screenshots.err
