
Install requirements:

```
brew install imagemagick
pip install -r requirements.txt
```

Modify com.jessealdridge.screenshots.plist, replace "/Users/jessealdridge" with your home directory.

Run `./launch.sh` will start taking screenshots and dump any error messages.
Assuming no horrible error messages appear, you can hit ctrl+c to kill the script.
(Note that screenshots will continue to be taken even after the script is killed.)

After running `launch.sh` once, the script should auto-start every time you boot your computer.

To stop taking screenshots run:

`launchctl unload ~/Library/LaunchAgents/com.jessealdridge.screenshots.plist`
