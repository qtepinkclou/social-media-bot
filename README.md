# **bananaBread**: _A Bot for Discord_

**bananaBread** is a Python library for managing a Discord Bot.

Scripts are written in Python 3.9.7

This project is under active development.

**Currently supported modules are**

1. _pydiscmd_
2. _getmedia_
3. __detect_landmark__

## **Changes Log**

- Created two different requirements.txt, added _pdoc3_ as a requirement.

- Primitive use of _config.py_ is implemented.

- Constants in each module correctly placed and named according to PEP8.

- Changed _pydiscmd.py_ structure. (Will be gathered under a single class soon)

- README file markup language changed from **.rst** to **.md**.

## **Identified Problems**

- _pdoc3_ cannot document most of the functions in _handle_discord_. Refer to script until fixed.

- Due to an error yet unknown, media downloads are sometimes halted, but does not break the code. Check terminal to ensure there is no error until it is fixed.

- Not sure which req.txt is more suitable so included both for now. (Fix is soon)

- Guide for _reStructuredText_ is used when writing docstrings. Therefore documentation may look a bit bizarre until fixed. (Fix is not soon)
