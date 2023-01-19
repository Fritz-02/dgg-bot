from dggbot import DGGBot
import time
from typing import Optional

bot = DGGBot(
    username="Bot",
    owner="Owner",
    wss="wss://chat.omniliberal.dev/ws",
    sid="SID",
)


# Command arguments
@bot.command()
def say(msg, arg: str):
    """Say whatever was typed after the command."""
    msg.reply(arg)


@bot.command()
def hug(msg, nick: Optional[str] = None, *_):
    """Hugs whoever/whatever is typed right after the command, or the user calling it.
    Only the first name/word after the command is included, rest is discarded."""
    msg.reply(f"TeddyPepe {nick if nick else msg.nick} TeddyPepe")


@bot.command()
def ignore(msg, username: str, reason: Optional[str] = None):
    """Ignores the username, with an optional reason given. (doesn't actually do anything)"""
    msg.reply(f"Ignoring {username}." + (f" Reason: {reason}" if reason else ""))
    # Could add some functionality to ignore any messages/commands from the given username outside of this example


@bot.command(["log"])
def logs(msg, username: Optional[str] = None, *_):
    """Link logs of given username, or command user's."""
    if not username:
        username = msg.nick
    msg.reply(f"https://rustlesearch.dev/?username={username}&channel=Destinygg")


# Custom command permissions
def is_cake(msg):
    """A check where only the user 'Cake' can use commands with this check"""
    return msg.nick == "Cake"


@bot.command()
@bot.check(is_cake)
def cake(msg):
    """Command can only be used by the user 'Cake'"""
    msg.reply("🎂")


bot.run_forever(origin="https://www.omniliberal.dev")
