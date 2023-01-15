class AccountTooYoung(Exception):
    pass


class Banned(Exception):
    pass


class DuplicateMessage(Exception):
    pass


class InvalidMessage(Exception):
    pass


class NeedLogin(Exception):
    pass


class NoPermission(Exception):
    pass


class NotFound(Exception):
    pass


class ProtocolError(Exception):
    pass


class SubMode(Exception):
    pass


class Throttled(Exception):
    pass


class TooManyConnections(Exception):
    pass
