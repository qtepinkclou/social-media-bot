# **bananaBread**: _A Bot for Discord_

**bananaBread** is a Python library for managing a Discord Bot.

This project is under active development.

**Currently supported modules are**

1. _pydiscmd_
2. _getmedia_
3. _detect_landmark_
4. _captcha_generator_ (to be used in _detect_landmark_ only at this point)

## **Notes to End Users**

- To be able to use this program, refer to [link](https://www.writebots.com/discord-bot-token/) for step by step configuration of your own discord bot. Add the bot to one of your servers and run _main.py_

- In order to use !detectLandmark bot command, you need to have your own Google Cloud account which should be authenticated as a service account then its credentials should be added as an environment variable. For more information refer to [link.](https://cloud.google.com/docs/authentication/production#windows)

## **Changes Log**

- Created two different requirements.txt, added _pdoc3_ as a requirement.

- _config.py_ is implemented.

- README file markup language changed from **.rst** to **.md**.

- Conformity to PEP8 acquired.

- Changed _pydiscmd.py_ structure. (Will be gathered under a single class soon)



## **Identified Problems**

- _pdoc3_ cannot document most of the functions in _handle_discord_. Refer to script until fixed.

- Due to an error yet unknown, media downloads are sometimes halted, but does not break the code. Check terminal to ensure there is no error until it is fixed.

- Not sure which req.txt is more suitable so included both for now. (Fix is soon)

- Guide for _reStructuredText_ is used when writing docstrings. Therefore documentation may look a bit bizarre until fixed. (Fix is not soon)
