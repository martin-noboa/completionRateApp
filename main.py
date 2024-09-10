"""Module to interact with system directory."""
import sys
import os
import warnings
from data import *
from pdfSingleton import PDFSingleton
from plot import *
from helper import directoryCheck
from datawarehouse import store

def principal():    
    """Main code."""
    if len(sys.argv) < 2:
        print("Usage: python script.py <date>")
        sys.exit(1)
    date = sys.argv[1]
    contextDirectory = os.path.join("resources", "context",date)
    graphDirectory =  os.path.join("resources", "graphs",date)
    directoryCheck(graphDirectory)
    # Populate each process with its respective data
    icd = Data("icd.csv",date,"ICD","Complete")
    ucd = Data("ucd.csv",date,"UCD","Completed")
    closing = Data("clscmt.csv",date,"Closing Docs","Completed", "Closing")
    commitment = Data("clscmt.csv",date,"Commitment Letter","Complete","Commitment")

    processes = [icd,ucd,closing,commitment]
    #store clean data
    cleanDf = []

    # Create pdf
    pdf = PDFSingleton(date=date, defaultConfig=True)
    pdf.addPage()
    pdf.addCoverletter()
    pdf.writeToPDF('title', "Weekly Completion Rate Report")
    dateRange = pdf.getTimeRange() 
    pdf.writeToPDF('subtitle', dateRange)
    pdf.writeToPDF('sectionHeader', "Report Context")
    contextFile = contextDirectory + "/context.txt"
    with open(contextFile, "r",encoding="utf-8") as file:
            globalContext = file.read()
    pdf.writeToPDF("body", globalContext) 
    counter = 0
    for process in processes:
        df = process.getData()
        cleanDf.append(df)
        plot = countplot(df,graphDirectory,process.getProcess())
        pdf.addPage()
        # title
        pdf.writeToPDF('sectionHeader', process.getProcess())
        #context
        context = process.getContext()
        if len(context) > 0:
            pdf.writeToPDF("body", context)
        # summary
        pdf.writeToPDF("body", process.toString())
        pdf.writeToPDF("body", process.businessToString())
        pdf.writeToPDF("body", process.getAverageWorktimes())
        #pdf.addPage()
        pdf.addImage(plot)
    pdf.build()
    store(cleanDf,date)

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    principal()
