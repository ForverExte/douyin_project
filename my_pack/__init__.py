from threading import Thread
import datetime


def threaded(func):
    def wrapper(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
    return wrapper


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')


def convert_timestamp_to_datetime(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp)
    formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time


