import sys
import warnings
from pdf import PDFSingleton  # Import the PDFSingleton class

def create_letterhead(pdf, WIDTH):
    pdf.image("./resources/header.png", 0, 0, WIDTH)

def create_title(title, pdf):
    # Add main title
    pdf.set_font('Helvetica', 'b', 20)  
    pdf.ln(30)
    pdf.write(5, title)
    pdf.ln(10)
    # Add date of report
    pdf.set_font('Helvetica', '', 14)
    pdf.set_text_color(r=128,g=128,b=128)
    #--------------------------------------------------------------------------------------- TO DO
    # change to use day of the folder instead of today
    today = datetime.now()
    week_ago = (today - timedelta(days=7))
    timePeriod = week_ago.strftime("%m/%d/%Y") + " - " + today.strftime("%m/%d/%Y")
    pdf.write(4, timePeriod)
    # Add line break
    pdf.ln(10)

def create_section(title, pdf,style='i'):
    # Add main title
    pdf.set_font('Helvetica', style, 16)  
    pdf.ln(5)
    pdf.write(5, title)
    pdf.ln(5)

def write_to_pdf(pdf, words):
    # Set text colour, font size, and font type
    pdf.set_text_color(r=0,g=0,b=0)
    pdf.set_font('Helvetica', '', 12)
    
    pdf.write(5, words)
    
    
    
def main():    
    warnings.filterwarnings("ignore")

    if len(sys.argv) < 2:
        print("Usage: python script.py <date>")
        sys.exit(1)

    date = sys.argv[1]
     # Initialize PDFSingleton
    pdf = PDFSingleton(date=date, defaultConfig=True)
    pdf.addPage()
    pdf.writeToPDF('title', "Completion Rate Report")
    dateRange = pdf.getTimeRange() 
    pdf.writeToPDF('subtitle', dateRange)
    pdf.writeToPDF('sectionHeader', "Report Context")
    with open("./context/context.txt", "r") as file:
            content = file.read()
    pdf.writeToPDF(pdf, content) 
    pdf.ln(10)
    # Closing
    create_section("Closing", pdf)
    with open("./context/closing.txt", "r") as file:
        content = file.read()
    write_to_pdf(pdf, content)
    pdf.ln(10)
    
    # Commitment
    create_section("Commitment", pdf)
    with open("./context/commitment.txt", "r") as file:
        content = file.read()
    write_to_pdf(pdf, content)
    pdf.ln(10)
    
    # ICD
    create_section("ICD", pdf)
    with open("./context/icd.txt", "r") as file:
        content = file.read()
    write_to_pdf(pdf, content)
    pdf.ln(10)
    
    # UCD
    create_section("UCD", pdf)
    with open("./context/ucd.txt", "r") as file:
        content = file.read()
    write_to_pdf(pdf, content)
    pdf.ln(10)
    
    # eFolder
    create_section("eFolder", pdf)
    with open("./context/efolder.txt", "r") as file:
        content = file.read()
    write_to_pdf(pdf, content)
    pdf.ln(10)

# Build PDF
    pdf.build()

    


if __name__ == "__main__":
    main()
