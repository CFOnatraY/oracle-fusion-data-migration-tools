# Compare to Fix Info Displayed

This module contains scripts to compare geography-related files used in Oracle Fusion data migration processes. The goal is to validate and align geography names and codes across different data sources and XML reports generated from Oracle.

## Structure
- `compare_geography_files.py`: Compares flat files with geography data.
- `compare_geography_triplets.py`: Compares geography triplets (city, state, country).
- `compare_input_with_converted_report.py`: Validates the converted output against the original input.
- `final_compare_with_right_blend.py`: Final comparison script that validates against the `RIGHT_BLEND` column.
- `scrape_xml.py`: Extracts information from Oracle-generated XML reports.
- Support files: `input_file.xlsx`, `geography_report.xlsx`, etc.

## Usage

1. Update the input files (`input_file.xlsx`, `xml_reference_report.xml`, etc.).
2. Run the desired script:
```bash
python compare_input_with_converted_report.py
```
3. Review the output and make the necessary corrections.