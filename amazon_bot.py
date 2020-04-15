from datetime import datetime
import requests
import shelve
import schedule
import time
import os
import xml.etree.ElementTree as ET

fire = u'\U0001F525' 

def is_url_amazon(url_string):
    if url_string and "www.amazon.com" in url_string:
        return True
    else:
        return False

def is_item_expired(item):
    title_msg = item.find('{https://www.ozbargain.com.au}title-msg')
    if title_msg is not None and ("type" in title_msg.attrib) and title_msg.attrib['type'] == "expired":
        return True
    return False

def telegram_bot_sendtext(bot_message):
    
    bot_chatID = os.environ['TELEGRAM_BOT_CHAT_ID']
    bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

def job():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("Running Alerts Job @ ", dt_string)

    with shelve.open('ozb.db') as db:
        r = requests.get('https://www.ozbargain.com.au/deals/feed')
        tree = ET.fromstring(r.text)
        for item in tree.iter('item'):
            title = item.find('title').text
            guid = item.find('guid').text.split(' ')[0]
            url = item.find('{https://www.ozbargain.com.au}meta').attrib['url']
            is_amazon = is_url_amazon(url)
            is_expired = is_item_expired(item)
            is_existing_deal = guid in db

            if is_amazon and not is_expired and not is_existing_deal:
                #print(fire + " : " + title + " : Is Amazon  -  " + str(is_amazon) + " : Is Expired  -  " + str(is_expired))
                msg = fire + "Amazon Deal Alert" + fire + " : " + title + " [" + url + "]"
                response = telegram_bot_sendtext(msg)
                print(response)

                # Persist using guid
                db[guid] = msg
    
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("Job Completed @ ", dt_string)

schedule.every(5).minutes.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
