 ## tiktok

 This script will periodically check tiktok for new videos posted by a user. Once found the video will be downloaded and posted to Telegram.

 It makes use of the python TikTokAPI wrapper - https://github.com/davidteather/TikTok-Api

 A proxy is required to ease the retrieval of videos. A free list can be found here - https://scrapingant.com/free-proxies/

 To run the script use `source ./start.sh` this will start and activate the VEnv, install playright then source environment variables from the .env file before running the script.

The script will read a time from `last_time.txt` and will check for the users last video, if it's posted after the time in the file then the video is downloaded and posted to Telgram and the file updated with the new time.