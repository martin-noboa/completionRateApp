import sys
import warnings
from dataTemplate import ICD, UCD, EFolder, Closing, Commitment # Import data extraction classes
from pdfSingleton import PDFSingleton

def dataAbstraction(abstract_class_instance, directory) -> dict:
    return abstract_class_instance.template(directory)

def main():    
    warnings.filterwarnings("ignore")
    if len(sys.argv) < 2:
        print("Usage: python script.py <date>")
        sys.exit(1)
    date = sys.argv[1]
    directory = "./" + date + "/"

    # Map process names to their respective class instances
    processes = {
        "ICD": {"instance": ICD(), "data": None},
        "UCD": {"instance": UCD(), "data": None},
        "EFolder": {"instance": EFolder(), "data": None},
        "Closing": {"instance": Closing(), "data": None},
        "Commitment": {"instance": Commitment(), "data": None},
    }
    
    # Populate each process with its respective data
    for process_name, process_info in processes.items():
        abstract_class_instance = process_info["instance"]  # Get the class instance
        processes[process_name]["data"] = dataAbstraction(abstract_class_instance, directory)  # Store the result in 'data'

    # Loop through the dictionary and access data for each process
    for process_name, process_info in processes.items():
        process_data = process_info["data"]
        
        # Print or access specific values
        print(f"\nProcess: {process_name}")
        print(f"Total Loans: {process_data['totalLoansCount']}")
        print(f"Completed Loans: {process_data['completedLoansCount']}")
        print(f"Business Exceptions: {process_data['businessExceptionsCount']}")
        print(f"Exceptions: {process_data['exceptionsCount']}")
        print(f"Completion Rate: {process_data['completionRate']}%")


def createPDF(date):
     # Initialize PDFSingleton
    pdf = PDFSingleton(date=date, defaultConfig=True)
    pdf.addPage()
    pdf.addCoverletter()
    pdf.writeToPDF('title', "Completion Rate Report")
    dateRange = pdf.getTimeRange() 
    pdf.writeToPDF('subtitle', dateRange)
    pdf.writeToPDF('sectionHeader', "Report Context")
    with open("./context/context.txt", "r") as file:
            content = file.read()
    pdf.writeToPDF("body", content) 
    # Closing
    pdf.writeToPDF('title', "Closing")
    with open("./context/closing.txt", "r") as file:
        content = file.read()
    pdf.writeToPDF("body", content)
    
    # Commitment
    pdf.writeToPDF('title', "Commitment")
    with open("./context/commitment.txt", "r") as file:
        content = file.read()
    pdf.writeToPDF("body", content)
    
    # ICD
    pdf.writeToPDF('title', "ICD")
    with open("./context/icd.txt", "r") as file:
        content = file.read()
    pdf.writeToPDF("body", content)
    
    # UCD
    pdf.writeToPDF('title', "UCD")
    with open("./context/ucd.txt", "r") as file:
        content = file.read()
    pdf.writeToPDF("body", content)
    
    # eFolder
    pdf.writeToPDF('title', "eFolder")
    with open("./context/efolder.txt", "r") as file:
        content = file.read()
    pdf.writeToPDF("body", content)

# Build PDF
    pdf.build()

    


if __name__ == "__main__":
    main()
