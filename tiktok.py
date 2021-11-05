import telegram
from time import sleep
from TikTokApi import TikTokApi
from datetime import datetime
import datetime
import logging
import os
logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')


def write_last_time(t):
    try:
        logging.info('Update last time file')
        with open('last_time.txt', 'w') as f:
            f.write(str(t))
    except Exception as e:
        logging.error(str(e))

def read_last_time():
    logging.info('Read last time file')
    with open('last_time.txt', 'r') as f:
        pre_time = int(f.read())
    return pre_time

def save_video(video_bytes):
    logging.info('Storing video')
    with open("video.mp4", "wb") as out:
        out.write(video_bytes)

def send_message():
    logging.info('Send Telegram message')
    try:   
        bot = telegram.Bot(token=BOT_TOKEN)
        bot.send_video(chat_id='-1001649391102', video=open('video.mp4', 'rb'), supports_streaming=True) # Park Bench Tips 
        # bot.send_video(chat_id='-1001456379435', video=open('video.mp4', 'rb'), supports_streaming=True) # Spanners Playground
    except Exception as e:
        print('Error sending screenshot')
        logging.error('Error sending Telegram message')
        logging.error(str(e))


def within_running_hours():
    timestamp = datetime.datetime.now().time() 

    # Check if a time is within running hours
    start = datetime.time(7, 30)
    end = datetime.time(22, 00)
    return (start <= timestamp <= end)


logging.info('Starting')
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_API_KEY')

verifyfp = 'verify_9cedeca1f88dbe1ee89b08524dc764ef'
logging.info('Create API instance')
last_api_req = 'Create'
sleep(5)
api = TikTokApi.get_instance(proxy="159.197.128.163:3128")

logging.info('Generate device id')
sleep(5)
last_api_req = 'Generate'
device_id = api.generate_device_id()

count = 1

while True:
    try:
        if within_running_hours():
            pre_time = read_last_time()
            tiktoks = ''

            logging.info('Get user tiktoks')
            last_api_req = 'User'
            tiktoks = api.by_username("ticktocktip", count=count, custom_verifyFp=verifyfp,use_test_endpoints=True)

            for tiktok in tiktoks:
                if tiktok['createTime'] != pre_time:
                    logging.info('New video so get video data')
                    sleep(5)
                    last_api_req = 'Video'
                    video_bytes = api.get_video_by_tiktok(tiktok, custom_device_id=device_id, custom_verifyFp=verifyfp)

                    save_video(video_bytes)             
                    send_message()
                    write_last_time(tiktok['createTime'])
                else:
                    logging.info('No new video')
        else:
            logging.info('Out of hours')
            # sleep for an additional 25 mins out of hours
            sleep(1500)

        sleep(350)

    except KeyboardInterrupt:
        logging.info('Keyboard interrupt')
        break
    except Exception as e:
        logging.error('General Exception')
        logging.info(str(e))
        logging.info(last_api_req)
        sleep(350)
        continue