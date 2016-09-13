
Install requirements:
```
brew install imagemagick
pip install -r requirements.txt
```

Modify com.jessealdridge.screenshots.plist, replace "/Users/jessealdridge" with your home directory.

Run `./launch.sh`

After running `launch.sh` once, the script should auto-start every time you boot your computer.

To stop taking screenshots run:
`launchctl unload ~/Library/LaunchAgents/com.jessealdridge.screenshots.plist`
