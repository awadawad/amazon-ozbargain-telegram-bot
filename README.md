# Amazon OzBargain Telegram Bot

Telegram Bot that scrapes OzBargains' atom feed for Aamazon deals.

## How to run the bot

### Create a bot

In order to run the bot, you'll first need to register a bot with the telegram's `botfather`. You'll then need a `bot_token` and the `chat_id` for that registered bot. For instructions on how to get those, simply follow the following [guide](https://medium.com/@ManHay_Hong/how-to-create-a-telegram-bot-and-send-messages-with-python-4cf314d9fa3e)

### Add environemt variables
Run the following in the terminal:

```
export TELEGRAM_BOT_CHAT_ID=<YOU_BOT_CHAT_ID>
export TELEGRAM_BOT_TOKEN=<YOUR_TOKEN_ID>
```

### Setup environment
Download dependencies by running pip3 in the shell:
```
python3 -m venv ./env
pip3 install -r requirements.txt
```

### Run script in the background

Simply execute the following in a terminal to run the script in the background (logs are outputted to `bot_out.log`)

```
nohup python -u ./amazon_bot.py > bot_out.log &
```

At 5 min intervals, the bot will call off to ozbargain to check if there are any new amazon deals.

To kill the bot simply run:
```
pkill -f amazon_bot.py
```