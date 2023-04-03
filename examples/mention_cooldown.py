"""
Example on how to implement a cooldown for non-commands, like mentions.
Inspiration from https://github.com/tenacious210/dggpt
"""
from dggbot import DGGBot
import time

bot = DGGBot("AUTH_TOKEN", owner="OWNER")
cooldown = 60  # seconds


@bot.mention()
def on_mention(msg):
    if bot._last_msg is not None:
        if time.time() - bot._last_msg[1] < cooldown:
            print("On cooldown")
            return
    # run your code


bot.run_forever()
