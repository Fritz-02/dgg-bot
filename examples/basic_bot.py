from dggbot import DGGBot
import time

bot = DGGBot("AUTH_TOKEN", username="Bot", owner="Owner")


@bot.command()
def mmmmphone(msg):
    """Replies with the following message."""
    msg.reply("📞 MMMM")


@bot.command(aliases=["obamna"])
def obamna_cmd(msg):
    msg.reply("OBAMNA LULW")


@bot.command()
@bot.is_owner()
def test(msg):
    """Test command that is restricted to only the bot owner."""
    msg.reply("Test 123")


"""
Events
You can either name the function after the event, or include the event name in the decorator.
mention() is also included as a shortcut for event("on_mention").

Event names: on_ban, on_broadcast, on_join, on_mention, on_msg, on_mute, on_privmsg, on_quit, on_refresh, on_unban
"""


@bot.event()
def on_msg(msg):
    print(msg)


# @bot.event("on_mention")
@bot.mention()
def yump(msg):
    if "MiyanoHype" in msg.data:
        time.sleep(0.5)
        msg.reply(f"{msg.nick} MiyanoHype")


while True:
    bot.run()
    time.sleep(2)
