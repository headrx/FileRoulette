FileRoulette
============
A script to seek and discover random files on various hosting services.

Introduction
------------
File-Roulette began as a toy project on the X9 Security Discord chat. The original goal was to find random uploadfile.io files by testing random urls to see if they were alive. Since then, we've been tweaking and updating the script, and have expanded it into something bigger than we had previously planned. This project is in a state of flux, constantly growing and evolving as we expand our scope and refine our skills.

Contributing
------------
If you're interested in contributing to this project, simply fork it and get to work!

Requirements
------------
* Python 3.5 or newer
* requests
* beautifulsoup4

Installation
------------
To use this software, it is advised that you set up a virtualenv. Once that's done, activate the virtualenv and run `pip install -r requirements.txt`. This will get your environment ready to run the application.

There are two main executable files currently in the root directory:
* `fileroulette.py`: The original FileRoulette script, with threading and support for a couple different targets. This file is outdated, but is being kept for the time being for use as reference as we develop the newer, modular code.
* `roulette.py`: The newer, modular code. Currently it does not support threading and only features one module (targeting uploadfiles.io), but it is under active development and will replace `fileroulette.py` in time.

It is advised that you use the `roulette.py` script instead of the `fileroulette.py` script, as it is under active development and your input can aid us in making the script better!

Feedback
--------
If you have any problems, suggestions, or other feedback, please open a new issue with the "Issues" tab above!
