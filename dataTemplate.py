'''Import req libraries'''
import pandas as pd
from abc import ABC, abstractmethod
CONTEXT_DIRECTORY = "./context/"

class dataTemplate(ABC):
    def template(self,directory,contextDirectoy):
        self.directory = directory
        self.contextDirectory = contextDirectoy
        self.data = {}
        self.data["rawData"] = self.loadData()
        self.data["cleanData"] = self.cleanData()
        self.data["totalLoansCount"] = self.getLoanCount()
        self.data["completedLoansCount"] = self.getCompletedLoans()
        self.data["businessExceptionsCount"] = self.getBusinessExceptions()
        self.data["exceptionsCount"] = self.getExceptions()
        self.data["completionRate"] = self.completionRate()
        self.data["context"] = self.getContext()
        self.data["processName"] = self.getProcessName()
        self.data["summary"] = self.toString()

        return self.data

    def completionRate(self) -> float:
        if self.data["totalLoansCount"] == 0:
            return 0
        totalLoans = self.data["completedLoansCount"] + self.data["businessExceptionsCount"]
        return float("{:.2f}".format((totalLoans/ self.data["totalLoansCount"])*100))

    def getLoanCount(self) -> int:
        return len(self.data["cleanData"])

    def cleanData(self) -> pd.DataFrame:
        drop = ['Resource', 'Worktime', 'ExceptionReason', 'Deferred']
        data = self.data["rawData"].drop(columns=drop)
        data['Loaded'] = pd.to_datetime(data['Loaded'])
        data['LastUpdated'] = pd.to_datetime(data['LastUpdated'])
        return data.groupby('Id')
    
    def getBusinessExceptions(self) -> int:
        '''Get count of business exceptions'''
        exceptions = self.data["cleanData"].apply(lambda group: group['Tags'].str.contains('Business Exception').sum())
        return exceptions.sum()

    def getExceptions(self) -> int:
        return self.data["totalLoansCount"] - (self.data["completedLoansCount"] + self.data["businessExceptionsCount"])
    
    def toString(self)->str:
        return ("Total Loans: " + str(self.data['totalLoansCount']) +
                "\nCompleted Loans: " + str(self.data['completedLoansCount']) +
                "\nBusiness Exceptions: " + str(self.data['businessExceptionsCount']) +
                "\nExceptions: " + str(self.data['exceptionsCount']) +
                "\nCompletion Rate: " + str(self.data['completionRate']) +"%")

    @abstractmethod
    def loadData(self) -> pd.DataFrame:
        # Read CSV file and store raw data
        pass

    @abstractmethod
    def getCompletedLoans(self) -> int:
        #  Get completed loans and count number of instances
        pass

    @abstractmethod
    def getContext(self) -> str:
        #  Get process context
        pass

    @abstractmethod
    def getProcessName(self) -> str:
        #  Get process context
        pass
    
class ICD(dataTemplate):
    def loadData(self)-> pd.DataFrame:
        filename = '/icd.csv'
        data = pd.read_csv(self.directory+filename)
        return data

    def getCompletedLoans(self)-> int:
        return self.data["cleanData"]['Status'].apply(lambda status: status == 'Complete').sum()
    
    def getContext(self) -> str:
        contextFile = self.contextDirectory + "/icd.txt"
        with open(contextFile, "r",encoding="utf-8") as file:
            context = file.read()
        return context
    
    def getProcessName(self) -> str:
        return "Initial and Final Closing Disclosures"

class UCD(dataTemplate):
    def loadData(self)-> pd.DataFrame:
        filename = '/ucd.csv'
        data = pd.read_csv(self.directory+filename)
        return data

    def getCompletedLoans(self)-> int:
        return self.data["cleanData"]['Status'].apply(lambda status: status == 'Completed').sum()
    
    def getContext(self) -> str:
        contextFile = self.contextDirectory + "/ucd.txt"
        with open(contextFile, "r",encoding="utf-8") as file:
            context = file.read()
        return context
    
    def getProcessName(self) -> str:
        return "UCD/LCLA"
    

class Closing(dataTemplate):
    def loadData(self)-> pd.DataFrame:
        filename = '/clscmt.csv'
        data = pd.read_csv(self.directory+filename)
        closing = data[data['Tags'].str.contains('Closing')]
        return closing

    def getCompletedLoans(self)-> int:
        return self.data["cleanData"]['Status'].apply(lambda status: status == 'Completed').sum()
    
    def getContext(self) -> str:
        contextFile = self.contextDirectory + "/closing.txt"
        with open(contextFile, "r",encoding="utf-8") as file:
            context = file.read()
        return context
    
    def getProcessName(self) -> str:
        return "Closing Docs"
    
class Commitment(dataTemplate):
    def loadData(self)-> pd.DataFrame:
        filename = '/clscmt.csv'
        data = pd.read_csv(self.directory+filename)
        commitment = data[data['Tags'].str.contains('Commitment')]
        return commitment

    def getCompletedLoans(self)-> int:
        return self.data["cleanData"]['Status'].apply(lambda status: status == 'Complete').sum()
    
    def getContext(self) -> str:
        contextFile = self.contextDirectory + "/commitment.txt"
        with open(contextFile, "r",encoding="utf-8") as file:
            context = file.read()
        return context
    
    def getProcessName(self) -> str:
        return "Commitment Letter"

    
class EFolder(dataTemplate):
    def loadData(self)-> pd.DataFrame:
        filename = '/efolder.csv'
        data = pd.read_csv(self.directory+filename)
        return data

    def getCompletedLoans(self)-> int:
        return self.data["cleanData"]['Status'].apply(lambda status: status == 'Complete').sum()
    
    def getContext(self) -> str:
        contextFile = self.contextDirectory + "/efolder.txt"
        with open(contextFile, "r",encoding="utf-8") as file:
            context = file.read()
        return context
    
    def getProcessName(self) -> str:
        return "eFolder"


