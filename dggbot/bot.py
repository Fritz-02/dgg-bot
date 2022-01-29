import itertools
import logging
from typing import List, Tuple, Union
from .event import EventType
from .message import Message, PrivateMessage
from .chat import DGGChat


class DGGBot(DGGChat):

    def __init__(self, auth_token=None, username=None, prefix='!'):
        super().__init__(auth_token=auth_token, username=username)
        self.prefix = prefix
        self._commands = {}
        self._mention = {}
        self._events = {}

    def command(self, name: str = None,
                aliases: Union[List[str], Tuple[str]] = tuple(),
                **kwargs):
        """Decorator to add commands to bot."""
        def decorator(func):
            for cmd_name in itertools.chain((name or func.__name__,), aliases):
                if cmd_name in self._commands:
                    raise Exception(f'Command name "{cmd_name}" already exists.')
                else:
                    self._commands[cmd_name] = func
            return func

        return decorator

    def mention(self, func):
        """Decorator to add auto-replies to bot."""
        self._mention[func.__name__] = func

    def on_mention(self, msg):
        for func in self._mention.values():
            if func(msg):
                break

    def on_msg(self, msg):
        if self.is_command(msg):
            self.on_command(msg)

    def is_command(self, msg: Message) -> bool:
        return msg.data.startswith(self.prefix)

    def on_command(self, msg: Message):
        cmd = msg.data.split(' ')[0][1:]
        if cmd in self._commands:
            self._commands[cmd](msg)
