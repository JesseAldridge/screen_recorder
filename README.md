
This tool will take a screenshot of your desktop once every five seconds.
Screenshots older than four days are deleted automatically.

Install requirements:

```
brew install imagemagick
brew install imagesnap
pip install --user -r requirements.txt
```

Modify `com.jessealdridge.screenshots.plist`, replace the `"/Users/jesse_aldridge/..."` paths as appropriate.

Stick the plist in your LaunchAgents dir:

`ln com.jessealdridge.screenshots.plist ~/Library/LaunchAgents/com.jessealdridge.screenshots.plist`

Launch the script:

`chmod +x launch.sh && ./launch.sh`.

This script will launch the screenshot loop and tail the logs so you can see if there are any errors.  
You can hit ctrl+c to kill the script.  
Screenshots will continue to be taken even after the launch script is killed.

After running `launch.sh` once, the recorder should auto-start every time you boot your computer.

To stop taking screenshots run:

`launchctl unload ~/Library/LaunchAgents/com.jessealdridge.screenshots.plist`

Using the default config, one screenshot will be taken every five seconds and six days of
screenshots will be stored.  They should take up about 10-20 GB worth of hard-drive space.

[MIT License](https://opensource.org/licenses/MIT)
