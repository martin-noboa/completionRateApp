"""Module to interact with system directory."""
import sys
import os
import warnings
from data import *
from pdfSingleton import PDFSingleton

def principal():    
    """Main code."""
    if len(sys.argv) < 2:
        print("Usage: python script.py <date>")
        sys.exit(1)
    date = sys.argv[1]
    #directory = "./resources/reports/" + date + "/"
    directory = os.path.join("resources", "reports", date)
    contextDirectory = os.path.join("resources", "context")
    # Populate each process with its respective data
    icd = Data(directory+"/icd.csv","ICD","Complete")
    ucd = Data(directory+"/ucd.csv","UCD","Completed")
    closing = Data(directory+"/clscmt.csv","Closing Docs","Completed")
    commitment = Data(directory+"/clscmt.csv","Commitment Letter","Complete")

    processes = [icd,ucd,closing,commitment]
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
        pdf.addPage()
        # title
        pdf.writeToPDF('sectionHeader', process.getProcess())
        #context
        context = process.getContext()
        if len(context) > 0:
            pdf.writeToPDF("body", context)
        # summary
        pdf.writeToPDF("body", process.toString())
        pdf.writeToPDF("body", process.getAverageWorktimes())
    pdf.build()
    

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    principal()
