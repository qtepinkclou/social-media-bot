# **bananaBread**: _A Bot for Social Media Platforms_

**bananaBread** is a Python library for managing a Social Media Bot.

This project is under active development.

**Currently supported modules are**

1. _media_getter_
2. _landmark_detector_
3. _captcha_tester_ (to be used before any feature if needed.)

## **Notes to End Users**

- This program is written in order to be usable for any conceivable social media platform, however only the wrapper for Discord is currently written and ready to go.

- To be able to use this program, refer to [link](https://www.writebots.com/discord-bot-token/) for step by step configuration of your own discord bot. Add the bot to one of your servers, add the private token for your bot inside your _.env_ file as shown in _.env.example_. Finally run _go_bananas_discord.py_

- In order to use !detectLandmark bot command and not get an auth error from google servers, upon running the bot, you need to have your own Google Cloud account which should be authenticated as a service account. After this process the json file provided by the google should be moved to src/features/landmark_detector directory and named as follows: _user_credentials.json_. For more information refer to [link.](https://cloud.google.com/docs/authentication/production#windows)

