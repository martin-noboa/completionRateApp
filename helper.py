from datetime import timedelta
import sys
import os

def secondsToTimedelta(value):
    minutes =value/60
    seconds = value%60
    timespan = timedelta(minutes=minutes,seconds=seconds)
    return timespan


def directoryCheck(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created.")
    else:
        print(f"Directory '{directory}' already exists.")
