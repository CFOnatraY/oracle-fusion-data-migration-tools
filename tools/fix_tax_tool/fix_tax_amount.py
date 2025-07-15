import os
import pandas as pd
import requests
import csv
from dotenv import load_dotenv
from time import sleep

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TOKEN_URL = os.getenv("TOKEN_URL")
API_BASE_URL = os.getenv("API_BASE_URL")
BASE_URL = os.getenv("BASE_URL")

# Read Excel file
df = pd.read_excel("transaction_number_template.xlsx")
transaction_numbers = df['TransactionNumber'].tolist()

def get_access_token():
    payload = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': f'{BASE_URL}/fscmRestApi'
    }
    response = requests.post(TOKEN_URL, data=payload)
    response.raise_for_status()
    return response.json().get('access_token')

def get_transaction_id(token, transaction_number):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{API_BASE_URL}/receivablesInvoices?q=TransactionNumber={transaction_number}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    items = response.json().get('items', [])
    return items[0]['CustomerTransactionId'] if items else None

def patch_transaction(token, transaction_id):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    url = f"{API_BASE_URL}/receivablesInvoices/{transaction_id}"
    body = {
        "TaxAmount": 0.00
    }
    response = requests.patch(url, json=body, headers=headers)
    return response.status_code, response.text

def main():
    token = get_access_token()
    log_rows = []

    for number in transaction_numbers:
        try:
            transaction_id = get_transaction_id(token, number)
            if transaction_id:
                status, message = patch_transaction(token, transaction_id)
                log_rows.append([number, transaction_id, status, message])
            else:
                log_rows.append([number, "Not Found", "Error", "Transaction not found"])
        except Exception as e:
            log_rows.append([number, "Error", "Exception", str(e)])
        sleep(1)  # Avoid throttling

    # Save log
    with open("output_log.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["TransactionNumber", "CustomerTransactionId", "Status", "Message"])
        writer.writerows(log_rows)

if __name__ == "__main__":
    main()
