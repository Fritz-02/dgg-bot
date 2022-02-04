DGG-bot
======

.. image:: https://img.shields.io/pypi/v/dgg-bot.svg
   :target: https://pypi.python.org/pypi/dgg-bot
   :alt: PyPI version info
.. image:: https://img.shields.io/pypi/pyversions/dgg-bot.svg
   :target: https://pypi.python.org/pypi/dgg-bot
   :alt: PyPI supported Python versions
A library for making a bot in Destiny.gg chat.

Installing
----------

**Python 3.7 or higher is required**

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U dgg-bot

    # Windows
    py -3 -m pip install -U dgg-bot


Examples
--------

A simple bot with two commands and will yump back at chatters. **Take care not to create a bot that will be a nuisance in chat, or you risk getting IP banned.**

.. code-block:: python

   from dggbot import DGGBot
   import time

   bot = DGGBot('AUTH_TOKEN', username='Username', owner='Owner', prefix="$")  # default command prefix is "!"

   @bot.command()
   @bot.is_owner()  # only the owner named above can use this command.
   def test(msg):  # $test
      msg.reply("Test 123")

   @bot.command(aliases=["banmeplease"])  # aliases for this command
   def banme(msg):  # $banme / $banmeplease
      bot.send("RightToBearArmsLOL BINGQILIN nathanTiny2")
      
   def is_cake(msg):  # a check where only the user Cake can use commands with this check
      return msg.nick == "Cake"
   
   @bot.command(aliases=["oooo"])
   @bot.check(is_cake)
   def pog(msg):
      msg.reply("Cake OOOO")
   
   @bot.mention()
   def yump(msg):
      if "MiyanoHype" in msg.data:
         time.sleep(0.5)
         msg.reply(f"{msg.nick} MiyanoHype")

   if __name__ == "__main__":
      while True:
         bot.run()
         time.sleep(2)
