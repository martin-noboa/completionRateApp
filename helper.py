from datetime import timedelta


def secondsToTimedelta(row):
    minutes =row["Worktime"]/60
    seconds = (row["Worktime"]%60)
    timespan = timedelta(minutes=minutes,seconds=seconds)
    row["Worktime"] = timespan