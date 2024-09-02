import pandas as pd

class Data:
    def __init__(self, path, process) -> None:
        self.path = path
        self.process = process
        self.rawData = None
        self.data = None

    def openFile(self):
        self.rawData = pd.read_csv(self.path)

    def getStatusCount(self, status):
        count, _ = self.data[self.data["Status"] == status].shape
        return str(count)

    def toString(self):
        print("Complete: " + self.getStatusCount("Complete"))
        print("Business Exception: " + self.getStatusCount("Business Exception"))
        print("Locked: " + self.getStatusCount("Locked"))
        print("Pending: " + self.getStatusCount("Pending"))
        print("Exception: " + self.getStatusCount("Exception"))

    def setStatus(self, row, completedKeyword):
        if pd.notnull(row["Tags"]) and "Business Exception" in row["Tags"]:
            row["Status"] = "Business Exception"
        elif row["isLocked"] == 1:
            row["Status"] = "Locked"
        elif row["Status"] == completedKeyword:
            row["Status"] = "Complete"
        elif row["Status"] == "Pending":
            pass
        else:
            row["Status"] = "Exception"
        return row

    def cleanUp(self, process, completedKeyword, dropColumns=None):
        if dropColumns is None:
            dropColumns = ['Resource', 'Loaded', 'LastUpdated', 'Exception', 'Deferred',
                           'Completed', 'KeyValue', 'Priority', 'Attempt', 'Locked', 
                           'ExceptionReason', 'isLocked']

        self.data = self.rawData.copy()
        self.data['isLocked'] = self.data['Locked'].apply(lambda x: 1 if pd.notnull(x) else 0)
        self.data['Status'] = self.data['Status'].apply(lambda x: x if pd.notnull(x) else "Pending")
        self.data = self.data.apply(lambda row: self.setStatus(row, completedKeyword), axis=1)
        self.data = self.data.drop(columns=dropColumns)
        self.data["Process"] = process
