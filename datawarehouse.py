import pandas as pd
import os

def store(dataframes,date):
    warehouse = os.path.join("resources","warehouse",date+".csv")
    print(warehouse)
    df = pd.concat(dataframes)
    df.to_csv(warehouse, encoding='utf-8', index=False, header=True)
    print("Warehouse updated.")

