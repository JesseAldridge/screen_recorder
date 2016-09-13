
Install requirements:

```
brew install imagemagick
pip install -r requirements.txt
```

Modify `com.jessealdridge.screenshots.plist`, replace `"/Users/jessealdridge"` with your home directory.

Run `chmod +x launch.sh && ./launch.sh`.  
This script will launch the screenshot loop and tail the logs so you can see if there are any errors.  
Assuming no horrible error messages appear, you can hit ctrl+c to kill the script.  
(Note that screenshots will continue to be taken even after the script is killed.)  

After running `launch.sh` once, the script should auto-start every time you boot your computer.

To stop taking screenshots run:

`launchctl unload ~/Library/LaunchAgents/com.jessealdridge.screenshots.plist`


[MIT License](https://opensource.org/licenses/MIT)
