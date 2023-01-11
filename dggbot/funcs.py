"""
Shared functions and whatnot for different classes.
"""
import threading


def threaded(func):
    """Decorator for making a threaded function."""

    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper
