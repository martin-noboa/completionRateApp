import pandas as pd
from abc import ABC, abstractmethod
CONTEXT_DIRECTORY = "./context/"

class dataTemplate(ABC):
    def template(self,directory):
        self.directory = directory
        self.data = {}
        """
        rawData : Dataframe
        cleanData : Dataframe
        completedItems : int
        exceptions : int
        businessExceptions : int
        """
        self.data["rawData"] = self.loadData()
        self.data["cleanData"] = self.cleanData()
        self.data["totalLoansCount"] = self.getLoanCount()
        self.data["completedLoansCount"] = self.getCompletedLoans()
        self.data["businessExceptionsCount"] = self.getBusinessExceptions()
        self.data["exceptionsCount"] = self.getExceptions()
        self.data["string"] = self.toString()

        return self.data
            


    def toString(self) -> str:
        if self.data["totalLoansCount"] == 0:
            return "No loans available to process."
        completionRate = self.data["completedLoansCount"] / self.data["totalLoansCount"]
        return f"Total items Commitment: {self.data['totalLoansCount']} \n Completed items: {self.data['completedLoansCount']} \n Completion rate: {completionRate:.2%}"

    def getLoanCount(self) -> int:
        return len(self.data["cleanData"])

    def cleanData(self) -> pd.DataFrame:
        drop = ['Resource', 'Worktime', 'ExceptionReason', 'Deferred']
        data = self.data["rawData"].drop(columns=drop)
        data['Loaded'] = pd.to_datetime(data['Loaded'])
        data['LastUpdated'] = pd.to_datetime(data['LastUpdated'])
        return data.groupby('Id')
    
    def getBusinessExceptions(self) -> int:
    # Apply the logic on each group after the data is grouped by 'Id'
        exceptions = self.data["cleanData"].apply(lambda group: group['Tags'].str.contains('Business Exception').sum())
        return exceptions.sum()


    def getExceptions(self) -> int:
        return self.data["totalLoansCount"] - (self.data["completedLoansCount"] + self.data["businessExceptionsCount"])

    @abstractmethod
    def loadData(self) -> pd.DataFrame:
        # Read CSV file and store raw data
        pass

    @abstractmethod
    def getCompletedLoans(self) -> int:
        #  Get completed loans and count number of instances
        pass

    
class ICD(dataTemplate):
    def loadData(self)-> pd.DataFrame:
        filename = 'icd.csv'
        data = pd.read_csv(self.directory+filename)
        return data

    def getCompletedLoans(self)-> int:
        return self.data["cleanData"]['Status'].apply(lambda status: status == 'Complete').sum()
    

class UCD(dataTemplate):
    def loadData(self)-> pd.DataFrame:
        filename = 'ucd.csv'
        data = pd.read_csv(self.directory+filename)
        return data

    def getCompletedLoans(self)-> int:
        return self.data["cleanData"]['Status'].apply(lambda status: status == 'Completed').sum()
    

class Closing(dataTemplate):
    def loadData(self)-> pd.DataFrame:
        filename = 'clscmt.csv'
        data = pd.read_csv(self.directory+filename)
        return data

    def getCompletedLoans(self)-> int:
        return self.data["cleanData"]['Status'].apply(lambda status: status == 'Completed').sum()
    
class Commitment(dataTemplate):
    def loadData(self)-> pd.DataFrame:
        filename = 'clscmt.csv'
        data = pd.read_csv(self.directory+filename)
        return data

    def getCompletedLoans(self)-> int:
        return self.data["cleanData"]['Status'].apply(lambda status: status == 'Complete').sum()
    
class EFolder(dataTemplate):
    def loadData(self)-> pd.DataFrame:
        filename = 'efolder.csv'
        data = pd.read_csv(self.directory+filename)
        return data

    def getCompletedLoans(self)-> int:
        return self.data["cleanData"]['Status'].apply(lambda status: status == 'Complete').sum()


