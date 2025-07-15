# Split CSV Tool

Utility script to split large CSV files into multiple smaller batches, facilitating partial uploads into Oracle Fusion.

## Included Files
- `split_csv.py`: Main script to split CSV files.
- `file_input.csv`: Input file to split.
- `ReceivablesCustomerProfile CuentasBillTo - lote X.csv`: Output batch files.

## Usage
1. Copy your original file and rename it to `file_input.csv`.
2. Run the script:
```bash
python split_csv.py
```
3. Output batch files will be generated in the same folder.