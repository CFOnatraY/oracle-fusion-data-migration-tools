# Oracle Fusion Data Migration Tools

This repository provides a suite of tools designed to support data cleaning, validation, transformation, and integration workflows related to Oracle Fusion Cloud Applications.

These tools were created to assist in the migration of customer, tax, geography, and pricing data into Oracle Fusion, ensuring consistency, accuracy, and format compliance.

---

## 🗂️ Structure

The repository is organized as follows:

```bash
oracle-fusion-data-migration-tools/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── shared_utils/               # Common utilities (e.g., __init__.py)
└── tools/                      # Main set of functional tools
    ├── compare_to_fix_info_displayed/
    ├── fix_tax_tool/
    ├── geocoded_tool/
    ├── migration_data_cleaning_tool/
    ├── price_list_tool/
    ├── scrape_state_city/
    └── split_csv_tool/
```

---

## 🔧 Tools Overview

Each folder under `tools/` includes its own `README.md`. Here's a summary:

| Tool Name | Description |
|-----------|-------------|
| [`compare_to_fix_info_displayed`](tools/compare_to_fix_info_displayed/) | Compares geography names and codes across source files and XML reports from Oracle. |
| [`fix_tax_tool`](tools/fix_tax_tool/) | Automates corrections to tax amounts and tax lines in Oracle Fusion invoices. |
| [`geocoded_tool`](tools/geocoded_tool/) | Validates and enriches geographic data using geocoding. |
| [`migration_data_cleaning_tool`](tools/migration_data_cleaning_tool/) | Cleans and transforms Excel files before uploading to Oracle Fusion. |
| [`price_list_tool`](tools/price_list_tool/) | Automates the upload of Pricing Strategies, Price Lists, and Discount Lists in Oracle Fusion using Selenium. |
| [`scrape_state_city`](tools/scrape_state_city/) | Scrapes XML or UI data from Oracle Fusion to retrieve city and state names. |
| [`split_csv_tool`](tools/split_csv_tool/) | Splits large CSV files into smaller batches for bulk upload. |

---

## 📦 Installation

1. Clone this repository:
	```bash
	git clone https://github.com/CFOnatraY/oracle-fusion-data-migration-tools.git
    git clone git@github.com:CFOnatraY/oracle-fusion-data-migration-tools.git
	```

2. Create a virtual environment (optional but recommended):
	```bash
	python -m venv venv
	```

3. Activate the virtual environment:
	- On Windows:
	```bash
	venv\Scripts\activate
	```
	- On macOS/Linux:
	```bash
	source venv/bin/activate
	```

## 🛠️ Requirements

Make sure you have Python 3.9 or above. To install the dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

To keep sensitive credentials out of source control, all secrets and credentials are loaded from a `.env` file.

Each tool that requires connection to Oracle Fusion APIs expects environment variables such as:

- `CLIENT_ID`
- `CLIENT_SECRET`
- `TOKEN_URL`
- `API_BASE_URL`
- `FUSION_USERNAME`
- `FUSION_PASSWORD`

👉 Refer to `.env.example` for the full list of required variables.

⚠️ Never commit your `.env` file. It is ignored via `.gitignore`.

## 🧪 How to Use

1. Navigate to the folder of the tool you want to use.
2. Follow the usage instructions in its `README.md`.
3. All tools are built to work with `.xlsx` or `.csv` files and are compatible with Oracle Fusion standards.

---

## 📂 Shared Utilities

The folder `shared_utils/` contains reusable functions or modules shared across tools. It can be extended with common data loaders, validators, or transformers.

---

## 🤝 Contributions

If you're part of a migration team or working on Oracle Fusion projects and want to contribute or reuse scripts, feel free to open a pull request or raise an issue.

---

## 🖥️ Environment Recommendations

Some tools in this repository—particularly [`price_list_tool`](tools/price_list_tool/)—leverage browser automation using Selenium and Google Chrome.

> 🛑 **Important:** These tools **require a local graphical environment (GUI)** for proper execution.

We recommend running these tools from a **native desktop environment** (such as Windows or macOS) rather than from headless or virtualized environments like WSL, Docker, or CI/CD runners, unless you have advanced configurations (e.g., WSLg or X11).

This ensures compatibility with:
- Manual login steps required by Oracle Fusion Cloud
- Visual interaction with Oracle UI modals and components
- ChromeDriver resolution via `webdriver-manager`

---

## 🔒 Internal Trace Prevention

This repository includes a pre-commit hook designed to prevent accidental commits of internal or confidential identifiers.

🛡️ For privacy and confidentiality, the terms being scanned (e.g., internal project codes or organization names) are **obfuscated** in the configuration (e.g., listed as `word1`, `word2`).

These hooks are implemented using [`pre-commit`](https://pre-commit.com/) and run automatically before every commit to enforce a **zero-trace policy**.

To enable them after cloning the repo:
```bash
pre-commit install
```
The hook logic is defined in:
- .pre-commit-config.yaml
- .hooks/check_obfuscated_terms.sh

✅ These scripts are safe to version and share publicly, as they do not expose any internal company data.

---

## 📄 License

This project is proprietary and intended for internal use within Oracle Fusion data migration contexts.

## ✍️ Author

Fernando Onatra