import datetime as dt
import threading

from send_images_text import *


def cycle_tasks(second: int, func):
    """Cycle send at a specific interval of seconds."""
    func()
    timer = threading.Timer(second, cycle_tasks, (second, func))
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