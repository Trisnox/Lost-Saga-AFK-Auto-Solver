

https://user-images.githubusercontent.com/66292369/214657905-d0662b63-b1b0-4a06-8805-c10d4d7e0227.mp4



# Lost-Saga-AFK-Auto-Solver
A macro to solve math that were caused by afk/speedhack/lobby lock. As an alternative for rtl (ritual).

After the script has been run, it will take a screenshot after each interval that has been provided. If the script finds the math box, then this script will read and answer that math.

This version has no difference from the main branch, only English translation is provided on this version.

# Usage
Install [python](https://www.python.org/downloads/), any version will do (recommended: 3.7>). For Windows 7, use [version 3.8.6](https://www.python.org/downloads/release/python-386/). For Windows XP, use [version 3.4.3](https://www.python.org/downloads/release/python-343/)

Go to [releases](https://github.com/Trisnox/Lost-Saga-AFK-Auto-Solver/releases) and choose version, then extract the file. Make sure all Python packages have been installed. If not, then run command prompt on that folder and type `pip install -U -r requirements.txt` to install all the required packages.

After that, install [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki), adding it to PATH is optional.

When all requirements have been met, use command prompt on that folder using admin privileges, then type `main.py`. When GUI appears, set the options as required, after you have set them, click the `start` button or `F6` on the keyboard.

# To-Do Priority
- [High] Automatic resolution. Since the math box always had the same size, the code must be rewritten so that it doesn't require a specific resolution, only the offsets are different on each resolution.
- [Low] Failproof. Ever since the latest version release, after a test, 100% out of 300+ images succeeded, it might require more tests. Since this script retries the math box if it cannot be read, this might not be required, except if the fail probability is high, then I will try to create a failproof method.
- [Low] One time usage. After being run, it only works if `F7` button is pressed and can be processed again until this script has been stopped. This is only made to synergize with jitbit macro recorder in order to create perfect macros with no math disturbance.
- [Low] If possible, I will bundle this script into an executable. This way, installing Python won't be needed, only Tesseract is required to be installed.

# QNA
Q: No input (enter/text), but OCR succeeded.\
A: ~~Try entering HQ, type something, and out. After this, it will usually work. ~~ After some research, run this script first, then run Lost Saga. I don't know why this script won't send input if Lost Saga is run first.

Q: On test input, `Enter` is pressed, but there is no `abc123` input.\
A: After you tried the solution above, this is a bug with `pynput`. However, it'll work fine for answering the math box, it is better to use `directinput`.

Q: It only prints `OCR failed to identify numbers, retrying`.\
A: It can be either\
   - The game window is partially cropped. When you use the `test screenshot` button, this is an example of a [good screenshot](https://media.discordapp.net/attachments/1097099248329306122/1097156717210501130/image.png), and this is an example of a [bad screenshot](https://media.discordapp.net/attachments/1097099248329306122/1097156850127999128/image.png) (notice how the bad screenshot had its top window blacked out, it is likely because the game resolution is higher than the desktop screen resolution)
   - Using incorrect resolution
   - Using incorrect window mode
   
   This problem might be fixed by the time the automatic resolution check has been released.

Q: Can it be used on other Lost Saga clients with different languages? \
A: Only for English/Indonesian clients. If you want to use it on another client, screenshot the math box ([usually looks like this](https://user-images.githubusercontent.com/66292369/215278517-69c7bb1f-1e73-4344-ad33-2d9b5de5663d.png)), crop the `enter` button, and then swap the component inside the `img` folder. If it doesn't work, then script modification might be needed.

Q: Error: `ModuleNotFoundError: No module named '...'`\
A: 2 possibilities.\
   1, haven't installed the module using `pip install -r requirements.txt`\
   2, have more than 1 Python version, you can check it using `py -0`. To use a specific version, type `py -python.version`, example: `py -3.10-64 main.py`
