"""Module to interact with system directory."""
import sys
import os
import warnings
from dataTemplate import *
from pdfSingleton import PDFSingleton

def dataAbstraction(dataInstance, directory, contextDirectory) -> None :
    """Instantiate dataTemplate abstract class."""
    return dataInstance.template(directory,contextDirectory)

def principal():    
    """Main code."""
    if len(sys.argv) < 2:
        print("Usage: python script.py <date>")
        sys.exit(1)
    date = sys.argv[1]
    #directory = "./resources/reports/" + date + "/"
    directory = os.path.join("resources", "reports", date)
    print(directory)
    contextDirectoy = os.path.join("resources", "context")
    print(contextDirectoy)

    # Populate each process with its respective data
    icd = dataAbstraction(ICD(),directory,contextDirectoy)
    ucd = dataAbstraction(UCD(),directory,contextDirectoy)
    efolder = dataAbstraction(EFolder(),directory,contextDirectoy)
    closing = dataAbstraction(Closing(),directory,contextDirectoy)
    commitment = dataAbstraction(Commitment(),directory,contextDirectoy)

    processes = [icd,ucd,efolder,closing,commitment]

    # Create pdf

    pdf = PDFSingleton(date=date, defaultConfig=True)
    pdf.addPage()
    pdf.addCoverletter()
    pdf.writeToPDF('title', "Weekly Completion Rate Report")
    dateRange = pdf.getTimeRange() 
    pdf.writeToPDF('subtitle', dateRange)
    pdf.writeToPDF('sectionHeader', "Report Context")
    contextFile =contextDirectoy + "/context.txt"
    with open(contextFile, "r",encoding="utf-8") as file:
            globalContext = file.read()
    pdf.writeToPDF("body", globalContext) 

    for process in processes:
        # title
        pdf.writeToPDF('title', process["processName"])
        #context
        pdf.writeToPDF("body", process["context"])
        # build expression
        pdf.writeToPDF("body", process["summary"])
    pdf.build()


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    principal()
