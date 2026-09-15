import time

def get_time():
    return time.localtime()

def format_time():
    now = get_time()

    return "{:02d}:{:02d}".format(
        now[3],
        now[4]
    )