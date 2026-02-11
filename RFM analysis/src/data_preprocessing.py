import pandas as pd
import os


def clean_data(df):
    df=df[df['Quantity']>0]
    df=df[df['UnitPrice']>0]
    df=df[df['CustomerID'].notna()]
    df['InvoiceDate']=pd.to_datetime(df['InvoiceDate'])
    return df

def create_total_col(df):
    df['Total']=df['UnitPrice']*df['Quantity']
    return df

def save_data(df):
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct path to data directory
    save_path = os.path.join(script_dir, 'data', 'clean_data.csv')
    df.to_csv(save_path, encoding='utf-8', index=False)
    return df

def show_details(df):
    print(f'Shape : {df.shape}')
    print(f'Info : {df.info()}')
    print(f'Null count : {df.isna().sum()}')
    print(f'Head : {df.head()}')

    return

def pipeline(df,save_bool=False,details_bool=False):
    df = clean_data(df)
    df = create_total_col(df)
    if save_bool:
        df = save_data(df)
    if details_bool:
        show_details(df)
    
    return df