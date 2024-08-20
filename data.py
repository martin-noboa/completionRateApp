import pandas as pd

def check_completion_cls(group):
    return 'Completed' in group['Status'].values
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