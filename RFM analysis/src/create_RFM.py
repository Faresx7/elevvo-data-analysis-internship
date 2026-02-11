import pandas as pd
import datetime as dt

def create_RFM_cols(df):
    '''
    this function takes Data-Frame have (InvoiceDate,InvoiceNo,Total)
    and create RFM pandas data frame on them by calculating:
    R:Recency
    F:Frequency
    M:Monetary
    
    :param df: Data-Frame have (InvoiceDate,InvoiceNo,Total) columns

    :output: RFM Data-Frame
    '''
    snapshot_date=df['InvoiceDate'].max() + dt.timedelta(days=1)

    rfm=df.groupby('CustomerID').agg({

        'InvoiceDate':lambda x: (snapshot_date-x.max()).days, #R
        'InvoiceNo':'count', #F
        'Total':'sum'
    })

    rfm=rfm.rename(columns={
    'InvoiceDate':'R',
    'InvoiceNo':'F',
    'Total':'M'
                })
    
    return rfm

def create_score(rfm_df):
    '''
    this function creates a score for each RFM number
    
    :param rfm_df: ready RFM table that don't have scores

    :output: full RFM Data-Frame the have scores and RF score to analyze behavior
    '''
    # labels descending because the lower R is the best
    rfm_df['R_score'] = pd.qcut(rfm_df['R'], q=5, labels=[5,4,3,2,1])

                        # rank to avoid problems related to redundancy in data
    rfm_df['F_score'] = pd.qcut(rfm_df['F'].rank(method='first'), q=5, labels=[1,2,3,4,5])

    rfm_df['M_score'] = pd.qcut(rfm_df['M'], q=5, labels=[1,2,3,4,5])

    # its better to usr R F in naming because we analysis person behavior
    rfm_df['RF_score'] = rfm_df['R_score'].astype('str') + rfm_df['F_score'].astype('str')

    return rfm_df

def create_customer_labels(rfm):
    '''
    this function creates label for each RF_score to make understanding
    buying behavior more easier for normal user
    
    :param rfm: RFM Data-Frame
    :rtype: Data-Frame
    '''
    
    seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',           
    r'33': 'need_attention',               
    r'[3-4][4-5]': 'loyal_customers',      
    r'41': 'promising',                    
    r'51': 'new_customers',                
    r'[4-5][2-3]': 'potential_loyalists',  
    r'5[4-5]': 'champions'          
}

    rfm['segments']=rfm['RF_score'].replace(seg_map,regex=True)
    return rfm

def rfm_pipeline(df,create_labels=False):
    '''
    pipeline combines all steps of creating RFM table
    
    :param df: Data-Frame have (InvoiceDate,InvoiceNo,Total) columns 
    :param create_labels: Bool, if user don't want to create labels
    :return: fully RFM table that have:
        R,F,M 
        R,F,M scores
        R,F score
        Labels for each R,F score
    :rtype: Data-Frame
    '''

    rfm = create_RFM_cols(df)
    rfm = create_score(rfm)
    if create_labels:
        rfm = create_customer_labels(rfm)
    return rfm