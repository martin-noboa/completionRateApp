import sys
import warnings
from pdf import PDFSingleton  # Import the PDFSingleton class
    
def main():    
    warnings.filterwarnings("ignore")

    if len(sys.argv) < 2:
        print("Usage: python script.py <date>")
        sys.exit(1)

    date = sys.argv[1]
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
