# Fix Tax Tool

This module automates the correction of tax-related issues in invoice records uploaded to Oracle Fusion Cloud Applications.

## Included Scripts
- `fix_invoice_patch_flow.py`: Orchestrates the full patching process in batch mode.
- `fix_tax_patch.py`: Applies tax patch to a specific invoice.
- `fix_tax_delete.py`: Deletes incorrect tax records.
- `fix_tax_amount.py`: Fixes incorrect tax amount values.

## Required Files
- `transaction_number_template.xlsx`: List of transaction numbers to process.
- `output_log_invoice_patch.csv`: Stores a log of execution results.

## Execution
```bash
python fix_invoice_patch_flow.py
```