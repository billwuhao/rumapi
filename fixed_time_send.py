import datetime as dt
import threading

from send_images_text import *


def cycle_send(second: int, *args):
    """Cycle send at a specific interval of seconds."""
    send_post(*args)
    print("Start sending")
    timer = threading.Timer(second, cycle_send, (second,*args))
    timer.start()


def get_second(itime: str):
    """Get the number of seconds between now and a specific time tomorrow.
    
    time: A specific time, like "06:00:00"(six o'clock)
    """
    now_time = dt.datetime.now()
    next_time = now_time + dt.timedelta(days=+1)
    next_year = next_time.date().year
    next_month = next_time.date().month
    next_day = next_time.date().day

    next_time = dt.datetime.strptime(
        str(next_year) + "-" + str(next_month) + "-" + str(next_day) +
        f" {itime}", "%Y-%m-%d %H:%M:%S")

    return (next_time - now_time).total_seconds()


def fixed_time_send(itime:str, *args):
    """Send regularly every day."""
    second = get_second(itime)
    # send_post(*args)
    # print("Start sending")
    timer = threading.Timer(second, send_post, args)
    print(f"Start sending after {second}s")
    timer.start()
    time.sleep(86399)
    cycle_send(86400, *args)