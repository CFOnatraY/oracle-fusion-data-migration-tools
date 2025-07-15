# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

def clean_data(input_file, output_file='clean_file.xlsx'):
    """
    This function reads an Excel file, cleans it by:
    - Stripping whitespace and tabs
    - Replacing empty strings with NaN
    - Sorting by key columns
    - Removing duplicates based on specific columns
    
    The cleaned data is saved to a new Excel file.
    
    :param input_file: Input file path (Excel format).
    :param output_file: Output file path to save the cleaned data.
    """
    # Load the Excel file
    df = pd.read_excel(input_file)

    # Clean the specific columns by removing leading/trailing whitespaces and tabs
    cols_to_clean = ['REVENUE_ACC_CODE_COMB', 'RECEIVABLE_ACC_CODE_COMB']
    for col in cols_to_clean:
        df[col] = df[col].astype(str).str.strip().replace({'': np.nan, 'nan': np.nan})

    # Create a completeness column that counts non-null values per row
    df['completeness'] = df.notna().sum(axis=1)

    # Sort by key columns and the completeness column
    df = df.sort_values(
        by=['CUSTOMER_NUMBER', 'CUST_SITE_NUMBER', 'PARTY_NAME', 'TAX_ID', 'completeness'],
        ascending=[True, True, True, True, False]
    )

    # Drop duplicates based on selected key columns, keeping the first (most complete) row
    df = df.drop_duplicates(subset=['CUSTOMER_NUMBER', 'CUST_SITE_NUMBER', 'PARTY_NAME', 'TAX_ID'], keep='first')

    # Remove the auxiliary 'completeness' column
    df = df.drop(columns='completeness')

    # Save the cleaned DataFrame to the output Excel file
    df.to_excel(output_file, index=False)

    print(f"Data cleaning complete. The cleaned file is saved as '{output_file}'.")

