import itertools
from typing import List, Tuple, Union, Callable
from .message import Message, PrivateMessage
from .chat import DGGChat


class DGGBot(DGGChat):

    def __init__(self, auth_token: str = None, username: str = None, owner: str = None, prefix='!'):
        super().__init__(auth_token=auth_token, username=username)
        self._owner = owner.lower()
        self.prefix = prefix
        self._commands = {}
        self._mention = {}
        self._events = {}

    def command(self, aliases: Union[List[str], Tuple[str]] = tuple(), *args, **kwargs):
        """
        Decorator to add commands to bot.
        :param aliases: aliases to call the function besides the function name
        :return:
        """
        def decorator(func: Callable):
            for cmd_name in itertools.chain((func.__name__,), aliases):
                if cmd_name in self._commands:
                    raise Exception(f'Command name "{cmd_name}" already exists.')
                else:
                    self._commands[cmd_name] = func
            return func

        return decorator

    def is_owner(self):
        """Decorator to add 'owner' permission required to a command."""
        def decorator(func: Callable):
            if not hasattr(func, "_perms"):
                func._perms = []
            perm = "owner"
            func._perms.append(perm)
            return func
        return decorator

    def mention(self):
        """Decorator to add auto-replies to bot."""
        def decorator(func):
            self._mention[func.__name__] = func
            return func
        return decorator

    def on_mention(self, msg: Message):
        for func in self._mention.values():
            if func(msg):
                break

    def on_msg(self, msg: Message):
        if self.is_command(msg):
            self.on_command(msg)

    def on_privmsg(self, msg: PrivateMessage):
        if self.is_command(msg):
            self.on_command(msg)

    def is_command(self, msg: Message) -> bool:
        return msg.data.startswith(self.prefix)

    def on_command(self, msg: Message):
        cmd = msg.data.split(' ')[0][1:]
        if cmd in self._commands:
            if hasattr(self._commands[cmd], "_perms"):
                perms = self._commands[cmd]._perms
                if "owner" in perms and msg.nick.lower() != self._owner:
                    return
            self._commands[cmd](msg)
