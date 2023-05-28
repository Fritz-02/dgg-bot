"""
Checks and tests for the following:
 - Connecting to DGG chat
 - (more to come whenever I think of more)
"""

import threading
import time

from dggbot import DGGChat


checks = {"connection": False}


class TestChat(DGGChat):
    def _on_open(self, ws):
        super()._on_open(ws)
        checks["connection"] = True


chat = TestChat()


# Test connection
t = threading.Thread(target=chat.run)
t.start()


# Close
time.sleep(5)
chat.ws.close()


for check, result in checks.items():
    print(f"{check}:", "SUCCESS" if result else "FAILURE")
