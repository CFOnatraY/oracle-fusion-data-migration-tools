import pandas as pd
import requests
import csv
from requests.auth import HTTPBasicAuth
from time import sleep
import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("FUSION_USERNAME")
PASSWORD = os.getenv("FUSION_PASSWORD")
BASE_URL = os.getenv("BASE_URL")

EXCEL_PATH = "TransactionNumber_template.xlsx"
OUTPUT_LOG = "output_log_invoice_patch.csv"

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def get_customer_transaction_id(txn_number):
    url = f"{BASE_URL}/fscmRestApi/resources/11.13.18.05/receivablesInvoices?q=TransactionNumber={txn_number}"
    r = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD), headers=headers)
    if r.ok and r.json().get("items"):
        return r.json()["items"][0]["CustomerTransactionId"]
    return None

def patch_invoice_status(customer_transaction_id, status="Incomplete"):
    url = f"{BASE_URL}/fscmRestApi/resources/11.13.18.05/receivablesInvoices/{customer_transaction_id}"
    r = requests.patch(url, json={"InvoiceStatus": status}, auth=HTTPBasicAuth(USERNAME, PASSWORD), headers=headers)
    return r.status_code, r.text

def get_invoice_lines(customer_transaction_id):
    url = f"{BASE_URL}/fscmRestApi/resources/11.13.18.05/receivablesInvoices/{customer_transaction_id}/child/receivablesInvoiceLines"
    r = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD), headers=headers)
    if r.ok:
        return [item["CustomerTransactionLineId"] for item in r.json().get("items", [])]
    return []

def patch_tax_amount_line(customer_transaction_id, line_id):
    url = f"{BASE_URL}/fscmRestApi/resources/11.13.18.05/receivablesInvoices/{customer_transaction_id}/child/receivablesInvoiceLines/{line_id}"
    r = requests.patch(url, json={"TaxAmount": 0.0}, auth=HTTPBasicAuth(USERNAME, PASSWORD), headers=headers)
    return r.status_code, r.text

df = pd.read_excel(EXCEL_PATH)
transaction_numbers = df['TransactionNumber'].astype(str).tolist()
log_rows = []

for txn_number in transaction_numbers:
    try:
        cust_txn_id = get_customer_transaction_id(txn_number)
        if not cust_txn_id:
            log_rows.append([txn_number, "", "", "", "Transaction ID not found"])
            continue

        status_incomplete, msg_incomplete = patch_invoice_status(cust_txn_id, "Incomplete")
        if status_incomplete != 200:
            log_rows.append([txn_number, cust_txn_id, "", "", f"Failed to mark incomplete: {msg_incomplete}"])
            continue

        line_ids = get_invoice_lines(cust_txn_id)
        if not line_ids:
            log_rows.append([txn_number, cust_txn_id, "", "", "No invoice lines"])
            continue

        for line_id in line_ids:
            status_line, msg_line = patch_tax_amount_line(cust_txn_id, line_id)
            log_rows.append([txn_number, cust_txn_id, line_id, "", f"PATCH TaxAmount: {status_line} - {msg_line}"])
            sleep(0.5)

        status_complete, msg_complete = patch_invoice_status(cust_txn_id, "Complete")
        log_rows.append([txn_number, cust_txn_id, "", "", f"Marked Complete: {status_complete} - {msg_complete}"])
        sleep(0.5)

    except Exception as e:
        log_rows.append([txn_number, "", "", "", f"Exception: {str(e)}"])

with open(OUTPUT_LOG, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["TransactionNumber", "CustomerTransactionId", "LineId", "TaxLineId", "Result"])
    writer.writerows(log_rows)
