from datetime import timedelta
import pandas as pd

def openFile(path):
    data = pd.read_csv(path)
    return data

def getStatusCount(data,status):
    count, _ = data[data["Status"] == status].shape
    return str(count)

def getWorktime(data):
    minutes = int(data["Worktime"]/60)
    seconds = (data["Worktime"]%60)
    timespan = timedelta(minutes=minutes,seconds=seconds)
    data["Worktime"] = timespan
    return data

def toString(data):
    print("Complete: " + getStatusCount(data,"Complete"))
    print("Business Exception: " + getStatusCount(data,"Business Exception"))
    print("Locked: " + getStatusCount(data,"Locked"))
    print("Pending " + getStatusCount(data,"Pending"))
    print("Exception " + getStatusCount(data,"Exception"))

def setStatus(data, completedKeyword):
    if pd.notnull(data["Tags"]) and "Business Exception" in data["Tags"]:
        data["Status"] = "Business Exception"
    elif data["isLocked"] == 1:
        data["Status"] = "Locked"
    elif data["Status"] == completedKeyword:
        data["Status"] = "Complete"
    elif data["Status"] == "Pending":
        pass
    else:
        data["Status"] = "Exception"
    return data

def cleanUp (data, process, completedKeyword, dropColumns=['Resource', 'Loaded','LastUpdated', 'Exception', 'Deferred','Completed','KeyValue','Priority','Attempt','Locked','ExceptionReason','isLocked']):
    data['isLocked'] = data['Locked'].apply(lambda x: 1 if pd.notnull(x) else 0)
    data['Status'] = data['Status'].apply(lambda x: x if pd.notnull(x) else "Pending")
    data = data.apply(lambda row: setStatus(row, completedKeyword), axis=1)
    data = data.drop(columns=dropColumns)
    data["Process"] = process
    return data