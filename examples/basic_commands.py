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


def is_admin(msg):
    """Check to restrict commands to only the following users."""
    return msg.nick in ("RightToBearArmsLOL", "Cake", "Destiny")


@bot.command(aliases=["admin"])
@bot.check(is_admin)
def admin_only_command(msg):
    msg.reply(f"{msg.nick} BINGQILIN nathanTiny2")


while True:
    bot.run()
    time.sleep(2)
