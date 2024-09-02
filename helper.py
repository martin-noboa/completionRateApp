from datetime import timedelta


    
def secondsToTimedelta(value):
    minutes =value/60
    seconds = value%60
    timespan = timedelta(minutes=minutes,seconds=seconds)
    return timespan