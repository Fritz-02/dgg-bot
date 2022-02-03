import json
import logging
from typing import Union
import websocket

from .event import EventType
from .message import Message, PrivateMessage, MuteMessage
from .errors import Banned, Throttled


class DGGChat:
    WSS = "wss://chat.destiny.gg/ws"
    URL = "https://www.destiny.gg"

    def __init__(self, auth_token=None, *, username: str = None):
        self.username = username.lower()
        self.ws = websocket.WebSocketApp(self.WSS, cookie=f'authtoken={auth_token}' if auth_token else None, on_open=self._on_open, on_message=self._on_message, on_error=self._on_error, on_close=self._on_close)
        self._connected = False

    def is_mentioned(self, msg: Union[Message, PrivateMessage]) -> bool:
        return False if self.username is None else (self.username in msg.data.lower())

    def on_mention(self, msg):
        """Do stuff when mentioned."""
        pass

    def on_broadcast(self, msg):
        """Do stuff when a BROADCAST is received."""
        pass

    def on_join(self, msg):
        """Do stuff when chatter joins."""
        pass

    def on_quit(self, msg):
        """Do stuff when chatter joins."""
        pass

    def on_ban(self, msg: Message):
        """Do stuff when a chatter is banned."""
        pass

    def on_unban(self, msg: Message):
        """Do stuff when a chatter is unbanned."""
        pass

    def on_mute(self, msg: MuteMessage):
        """Do stuff when a chatter is muted."""
        pass

    def on_refresh(self, msg: Message):
        """Do stuff when refreshed."""
        pass

    def on_msg(self, msg: Message):
        """Do stuff when a MSG is received."""
        pass

    def on_privmsg(self, msg: PrivateMessage):
        """Do stuff when a PRIVMSG is received."""
        pass

    def _on_message(self, ws, message: str):
        event_type, data = message.split(maxsplit=1)
        data = json.loads(data)
        if event_type == EventType.MESSAGE:
            msg = Message(self, event_type, data['nick'], data['features'], data['timestamp'], data['data'])
            self.on_msg(msg)
            if self.is_mentioned(msg):
                self.on_mention(msg)
        elif event_type == EventType.PRIVMSG:
            msg = PrivateMessage(self, event_type, data['nick'], timestamp=data['timestamp'], data=data['data'], message_id=data['messageid'])
            self.on_privmsg(msg)
            if self.is_mentioned(msg):
                self.on_mention(msg)
        elif event_type == EventType.BROADCAST:
            msg = Message(self, event_type, timestamp=data['timestamp'], data=data['data'])
            self.on_broadcast(msg)
        elif event_type == EventType.NAMES:
            logging.debug(f"{event_type} {data}")
        elif event_type in (EventType.JOIN, EventType.QUIT):
            msg = Message(self, event_type, data['nick'], data['features'], data['timestamp'])
            if event_type == EventType.JOIN:
                self.on_join(msg)
            else:
                self.on_quit(msg)
        elif event_type == EventType.BAN:
            msg = Message(self, event_type, data['nick'], data['features'], data['timestamp'], data['data'])
            self.on_ban(msg)
        elif event_type == EventType.UNBAN:
            msg = Message(self, event_type, data['nick'], data['features'], data['timestamp'], data['data'])
            self.on_unban(msg)
        elif event_type == EventType.MUTE:
            msg = MuteMessage(self, event_type, data['nick'], data['features'], data['timestamp'], data['data'], data['duration'])
            self.on_mute(msg)
        elif event_type == EventType.REFRESH:
            msg = Message(self, event_type, data['nick'], data['features'], data['timestamp'])
            self.on_refresh(msg)
        elif event_type in (EventType.PRIVMSGSENT, EventType.REFRESH):
            pass
        elif event_type == EventType.ERROR:
            if data['description'] == 'throttled':
                raise Throttled
            elif data['description'] == "banned":
                raise Banned
            else:
                logging.error(event_type, data)
                raise Exception(data['description'])
        else:
            logging.warning(f'Unknown event type: {event_type} {data}')

    def _on_open(self, ws):
        logging.info(f'Connecting to: {self.WSS}')
        self._connected = True

    def _on_close(self, ws, *_):
        logging.debug(f'Connection closed.')
        self._connected = False

    def _on_error(self, ws, error):
        logging.error(error)

    def run(self):
        self.ws.run_forever(origin=self.URL)

    def send(self, msg: str):
        """Send a message to chat."""
        payload = {'data': msg}
        self.ws.send(f'MSG {json.dumps(payload)}')

    def send_privmsg(self, nick: str, msg: str):
        """Send private message to someone."""
        payload = {"nick": nick, "data": msg}
        self.ws.send(f'PRIVMSG {json.dumps(payload)}')
