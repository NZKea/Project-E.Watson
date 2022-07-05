import time


def get_time():
    timestamp = float(str(time.time()).split(".")[0])
    return timestamp
