from fpdf import FPDF
import time
import pandas as pd
import sys
from datetime import datetime,timedelta
import warnings


# Global Variables
TITLE = "Weekly Completion Rate Report"
WIDTH = 210
HEIGHT = 297

def check_completion_cls(group):
    return '8 - All Complete' in group['Status'].values
def check_completion_cmt(group):
    return 'Complete' in group['Status'].values
def check_completion_icd(group):
    return 'Complete' in group['Status'].values
def check_completion_ucd(group):
    return 'Completed' in group['Status'].values
def check_completion_efolder(group):
    return 'Complete' in group['Status'].values
# ICD
def get_icd_data(directory):
    filename = 'icd.csv'
    data = pd.read_csv(directory+filename)
    drop = ['Resource', 'Worktime', 'ExceptionReason', 'Deferred']
    data = data.drop(columns=drop)
    data['Loaded'] = pd.to_datetime(data['Loaded'])
    data['LastUpdated'] = pd.to_datetime(data['LastUpdated'])
    grouped_icd = data.groupby('Id')
    icd_completion_status = grouped_icd.apply(check_completion_icd)
    total_items = len(icd_completion_status)
    completed_items = icd_completion_status.sum()
    completion_rate = completed_items / total_items
    icd = f"Total items: {total_items} \n Completed items: {completed_items} \n Completion rate: {completion_rate:.2%}"
    return icd
# UCD
def get_ucd_data(directory):
    filename = 'ucd.csv'
    data = pd.read_csv(directory+filename)
    drop = ['Resource', 'Worktime', 'ExceptionReason', 'Deferred']
    data = data.drop(columns=drop)
    data['Loaded'] = pd.to_datetime(data['Loaded'])
    data['LastUpdated'] = pd.to_datetime(data['LastUpdated'])
    ucd = data[~data['Tags'].str.contains('UCD/LCLA')]
    grouped_icd = data.groupby('Id')
    ucd_completion_status = grouped_icd.apply(check_completion_ucd)
    total_items = len(ucd_completion_status)
    completed_items = ucd_completion_status.sum()
    completion_rate = completed_items / total_items
    ucd = f"Total items: {total_items} \n Completed items: {completed_items} \n Completion rate: {completion_rate:.2%}"
    return ucd
#Closing and Commitment
def get_closing_commitment_data(directory):
    filename = 'clscmt.csv'
    data = pd.read_csv(directory+filename)
    drop = ['Resource', 'Worktime', 'ExceptionReason', 'Deferred']
    data = data.drop(columns=drop)
    data['Loaded'] = pd.to_datetime(data['Loaded'])
    data['LastUpdated'] = pd.to_datetime(data['LastUpdated'])
    closing = data[data['Tags'].str.contains('Closing')]
    grouped_closing = closing.groupby('Id')
    cls_completion_status = grouped_closing.apply(check_completion_cls)
    total_cls = len(cls_completion_status)
    completed_cls = cls_completion_status.sum()
    completion_cls = completed_cls / total_cls
    closing = f"Total items Closing: {total_cls} \n Completed items: {completed_cls} \n Completion rate: {completion_cls:.2%}"
    commitment = data[data['Tags'].str.contains('Commitment')]
    grouped_commitment  = commitment.groupby('Id')
    cmt_completion_status = grouped_commitment.apply(check_completion_cmt)
    total_cmt = len(cmt_completion_status)
    completed_cmt = cmt_completion_status.sum()
    completion_cmt = completed_cmt / total_cmt
    commitment = f"Total items Commitment: {total_cmt} \n Completed items: {completed_cmt} \n Completion rate: {completion_cmt:.2%}"
    return closing, commitment
# eFolder
def get_efolder_data(directory):
    filename = 'efolder.csv'
    data = pd.read_csv(directory+filename)
    drop = ['Resource', 'Worktime', 'ExceptionReason', 'Deferred']
    data = data.drop(columns=drop)
    data['Loaded'] = pd.to_datetime(data['Loaded'])
    data['LastUpdated'] = pd.to_datetime(data['LastUpdated'])
    grouped_efolder = data.groupby('Id')
    efolder_completion_status = grouped_efolder.apply(check_completion_efolder)
    total_items = len(efolder_completion_status)
    completed_items = efolder_completion_status.sum()
    completion_rate = completed_items / total_items
    efolder = f"Total items: {total_items} \n Completed items: {completed_items} \n Completion rate: {completion_rate:.2%}"
    return efolder



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
    pdf.ln(10)
    pdf.write(5, title)
    pdf.ln(10)

def write_to_pdf(pdf, words):
    
    # Set text colour, font size, and font type
    pdf.set_text_color(r=0,g=0,b=0)
    pdf.set_font('Helvetica', '', 12)
    
    pdf.write(5, words)
    
    
    
def main():    
    warnings.filterwarnings("ignore")
    directory = "./" + sys.argv[1] + "/"
    # Create PDF
    pdf = FPDF() # A4 (210 by 297 mm)
    # Add Page
    pdf.add_page()

    # Add lettterhead and title
    create_letterhead(pdf, WIDTH)
    create_title(TITLE, pdf)

    # Set context
    create_section("Report Context", pdf,'')
    file = open("context.txt", "r")
    content = file.read()
    file.close()
    write_to_pdf(pdf, content)
    pdf.ln(2)
    
    #closing
    create_section("Closing", pdf)
    closing,commitment = get_closing_commitment_data(directory)
    write_to_pdf(pdf, closing)
    #commitment
    create_section("Commitment", pdf)
    write_to_pdf(pdf, commitment)
    #icd
    create_section("ICD", pdf)
    icd = get_icd_data(directory)
    write_to_pdf(pdf, icd)
    #ucd
    create_section("UCD", pdf)
    ucd = get_ucd_data(directory)
    write_to_pdf(pdf, ucd)
    #efolder
    create_section("eFolder", pdf)
    efolder = get_efolder_data(directory)
    write_to_pdf(pdf, efolder)
    
    # Generate the PDF
    today = time.strftime("%d_%m_%Y")
    pdf.output("completionRateReport_"+today+".pdf")

if __name__ == "__main__":
    main()
