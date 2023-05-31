import time
from typing import Union

from dggbot import DGGBot, Message, MuteMessage, PrivateMessage

bot = DGGBot("AUTH_TOKEN", owner="Owner")


@bot.event()
def on_msg(msg: Message):
    """Prints the chat messages."""
    print(f"{msg.nick}: {msg.data}")


@bot.event("on_privmsg")
def whispered(msg: PrivateMessage):
    """Prints the whispered message."""
    print(f"{msg.nick} whispered to you: {msg.data}")


@bot.event("on_ban")
@bot.event("on_mute")
def ducked(msg: Union[Message, MuteMessage]):
    """Types DuckerZ at the chatter who was banned or muted."""
    time.sleep(1)
    msg.reply(f"{msg.data} DuckerZ")


trigger = True


def trigger_once(msg):
    return trigger


@bot.event()
@bot.check(trigger_once)
def on_join(msg):
    global trigger
    if msg.nick == "vyneer":
        msg.reply("> vyneer in chat nathanWeeb MiyanoHype")
        trigger = False


bot.run_forever()
