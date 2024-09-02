import pandas as pd
import os
from helper import *

class Data:
    def __init__(self, path, process,completedKeyword) -> None:
        self.path = path
        self.process = process
        self.completedKeyword = completedKeyword
        self.openFile()
        self.cleanUp()

    def openFile(self):
        self.rawData = pd.read_csv(self.path)

    def getStatusCount(self, status):
        count, _ = self.data[self.data["Status"] == status].shape
        return count


    def toString(self):
        complete = self.getStatusCount("Complete")
        be = self.getStatusCount("Business Exception")
        exception = self.getStatusCount("Exception")
        total =  complete + be + exception
        completionRate = float("{:.2f}".format((complete + be)/ total*100))
        return ("Total instances: " + str(total) +
                "\nCompleted: " + str(complete) +
                "\nBusiness Exceptions: " + str(be) +
                "\nExceptions: " + str(exception) +
                "\nCompletion Rate: " + str(completionRate) + "%")

    def getContext(self):        
        contextDirectory = os.path.join("resources", "context")
        contextFile = contextDirectory +  "/" + self.process + ".txt"
        with open(contextFile, "r",encoding="utf-8") as file:
            context = file.read()
        return context
    
    def averageWorktime(self,status=None):
        if status is None:
            return round(self.data["Worktime"].mean())
        else:
            try:
                return round(self.data[self.data["Status"] == status]["Worktime"].mean())
            except:
                return 0

        
    def getAverageWorktimes(self):
        total = secondsToTimedelta(self.averageWorktime())
        complete = secondsToTimedelta(self.averageWorktime("Complete"))
        businessExceptions = secondsToTimedelta(self.averageWorktime("Business Exception"))
        exceptions = secondsToTimedelta(self.averageWorktime("Exception"))
        return ("Average worktime for all instances: " + str(total) +
                "\nAverage worktime completions: " + str(complete) +
                "\nAverage worktime business exceptions: " + str(businessExceptions) +
                "\nAverage worktime for exceptions: " + str(exceptions))
        pass

    def setStatus(self, row):
        if pd.notnull(row["Tags"]) and "Business Exception" in row["Tags"]:
            row["Status"] = "Business Exception"
        elif row["isLocked"] == 1:
            row["Status"] = "Locked"
        elif row["Status"] == self.completedKeyword:
            row["Status"] = "Complete"
        elif row["Status"] == "Pending":
            pass
        else:
            row["Status"] = "Exception"
        return row

    def cleanUp(self, dropColumns=None):
        if dropColumns is None:
            dropColumns = ['Resource', 'Loaded', 'LastUpdated', 'Exception', 'Deferred',
                           'Completed', 'KeyValue', 'Priority', 'Attempt', 'Locked', 
                           'ExceptionReason', 'isLocked']

        self.data = self.rawData.copy()
        self.data['isLocked'] = self.data['Locked'].apply(lambda x: 1 if pd.notnull(x) else 0)
        self.data['Status'] = self.data['Status'].apply(lambda x: x if pd.notnull(x) else "Pending")
        self.data = self.data.apply(lambda row: self.setStatus(row), axis=1)
        self.data = self.data.drop(columns=dropColumns)
        self.data["Process"] = self.process


    def getProcess(self):
        return self.process
