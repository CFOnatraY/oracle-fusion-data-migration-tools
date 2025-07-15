import pandas as pd
import re

def update_migrated_data(clean_file, report_file, output_file='updated_clean_file.xlsx'):
    # Load the clean file and the report file
    df_clean = pd.read_excel(clean_file)
    df_report = pd.read_excel(report_file)

    # Create new columns for updated SITE_NUMBER and CHANGE_STATUS
    df_clean['NEW_SITE_NUMBER'] = None
    df_clean['CHANGE_STATUS'] = 'DON\'T EXIST'  # Default is "DON'T EXIST"
    df_clean['SUFFIX_ADDED'] = None

    # Additional columns for new data
    df_clean['NEW_PARTY_NUMBER'] = None
    df_clean['NEW_USO'] = None
    df_clean['NEW_CXC'] = 'NO CXC'  # Default value for missing account
    df_clean['NEW_CXI'] = 'NO CXI'  # Default value for missing account
    df_clean['NEW_FECHAFIN'] = None
    df_clean['NEW_ACCOUNT_NUMBER'] = None

    for idx, row in df_clean.iterrows():
        cust_site_number = str(row['CUST_SITE_NUMBER'])  # Ensure it's treated as a string
        
        # Try to find an exact match in the report file
        matching_row = df_report[df_report['SITE_NUMBER'].astype(str) == cust_site_number]
        
        if not matching_row.empty:
            # Exact match found, no change
            df_clean.at[idx, 'NEW_SITE_NUMBER'] = matching_row.iloc[0]['SITE_NUMBER']
            df_clean.at[idx, 'CHANGE_STATUS'] = 'NOT CHANGE'
        else:
            # Use a regular expression to find any number of digits appended to the end of the cust_site_number
            matching_row = df_report[df_report['SITE_NUMBER'].astype(str).str.startswith(cust_site_number)]
            
            if not matching_row.empty:
                # A match is found with digits appended at the end (could be 1, 2, or more digits)
                # We need to further check if the extra digits are numeric
                for site_number in matching_row['SITE_NUMBER'].astype(str):
                    # Check if the suffix is numeric and has at least 1 extra digit
                    suffix = site_number[len(cust_site_number):]
                    if suffix.isdigit() and len(suffix) > 0:
                        df_clean.at[idx, 'NEW_SITE_NUMBER'] = site_number
                        df_clean.at[idx, 'CHANGE_STATUS'] = 'CHANGE'
                        df_clean.at[idx, 'SUFFIX_ADDED'] = suffix
                        break  # Stop after finding the first valid match

        # Convert the 'NEW_SITE_NUMBER' in the clean file to string to ensure consistency
        df_clean['NEW_SITE_NUMBER'] = df_clean['NEW_SITE_NUMBER'].astype(str)

        # Now add additional columns from reference report
        matching_row = df_report[df_report['SITE_NUMBER'].astype(str) == df_clean.at[idx, 'NEW_SITE_NUMBER']]
        
        if not matching_row.empty:
            # Assign PARTY_NUMBER to NEW_PARTY_NUMBER
            df_clean.at[idx, 'NEW_PARTY_NUMBER'] = matching_row.iloc[0]['PARTY_NUMBER']
            
            # For USO, check if there's both "bill to" and "ship to"
            uso_values = matching_row['USO'].unique()
            if len(uso_values) > 1:
                df_clean.at[idx, 'NEW_USO'] = "BILL TO/SHIP TO"
            else:
                df_clean.at[idx, 'NEW_USO'] = uso_values[0]

            # Check for CXC (if exists)
            if 'CXC' in matching_row.columns:
                df_clean.at[idx, 'NEW_CXC'] = matching_row.iloc[0]['CXC']
            else:
                df_clean.at[idx, 'NEW_CXC'] = 'DON\'T_HAVE'

            # Check for CXI (if exists)
            if 'CXI' in matching_row.columns:
                df_clean.at[idx, 'NEW_CXI'] = matching_row.iloc[0]['CXI']
            else:
                df_clean.at[idx, 'NEW_CXI'] = 'DON\'T_HAVE'

            # Assign FECHAFIN to NEW_FECHAFIN
            df_clean.at[idx, 'NEW_FECHAFIN'] = matching_row.iloc[0]['FECHAFIN']

            # Assign ACCOUNT_NUMBER to NEW_ACCOUNT_NUMBER
            if 'ACCOUNT_NUMBER' in matching_row.columns:
                df_clean.at[idx, 'NEW_ACCOUNT_NUMBER'] = matching_row.iloc[0]['ACCOUNT_NUMBER']
            else:
                df_clean.at[idx, 'NEW_ACCOUNT_NUMBER'] = 'DON\'T_HAVE'

    # Save the updated data to a new file
    df_clean.to_excel(output_file, index=False)
    print(f"Data updating complete. The updated file is saved as '{output_file}'.")

