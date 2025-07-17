# 🧰 Oracle Fusion Pricing Strategies Automation

Automates the bulk upload of *Pricing Strategies* in Oracle Fusion Cloud Applications using Selenium WebDriver.

---

## 📁 Project Structure

```
price_list_tool/
├── pricing_strategies.xlsx                  # Source file with strategies and associated lists
├── step1_navigate_to_manage_pricing_strategy.py
├── step2_navigate_to_edit_pricing_strategy_(ps).py
├── step3_navigate_to_ps_edit_price_lists_(pl).py
├── step4_final_script_navigate_to_edit_pl_and_discount_lists_(dl).py
├── step5_navigate_to_edit_dl_and_currency_lists_(cl)_try1.py     # Not functional due to modal issue
├── step5_navigate_to_edit_dl_and_currency_lists_(cl)_try2.py     # Not functional due to modal issue
```

---

## 🚀 Key Scripts Overview

| Script | Description |
|--------|-------------|
| `step1_navigate_to_manage_pricing_strategy.py` | Navigates from Oracle Fusion Home to the "Manage Pricing Strategies" screen. Requires manual login. |
| `step2_navigate_to_edit_pricing_strategy_(ps).py` | Opens a specific strategy (column `Name`) from Excel to verify its presence in the UI. |
| `step3_navigate_to_ps_edit_price_lists_(pl).py` | For each strategy in the Excel file, adds multiple *Price Lists* and sets today's date as the start date. |
| `step4_final_script_navigate_to_edit_pl_and_discount_lists_(dl).py` | Final working script: adds *Price Lists* and *Discount Lists* for each strategy, with start dates. Skips entries marked as “NO APLICA”. |

---

## 📄 Excel File Format: `pricing_strategies.xlsx`

This file should contain the following columns:

| Pricing Strategy | Price List | Discount List | Currency Conversion List |
|------------------|------------|----------------|---------------------------|
| CED_ABC_001      | PL1        | DL1            | NO APLICA                |
| CED_ABC_001      | PL2        | DL1            | NO APLICA                |
| CED_DEF_002      | PL3        | NO APLICA      | NO APLICA                |

> 🔸 *The “Currency Conversion List” column is currently ignored because the `step5` scripts could not overcome a mandatory modal warning.*

---

## 📦 Requirements

- Python 3.10+
- Google Chrome
- Dependencies (install with `pip`):

```bash
pip install selenium webdriver-manager pandas openpyxl
```

---

## 🧪 How to Use

1. **Edit the Excel file** with your strategy and list data.
2. Run the scripts in sequence, or run the final `step4` directly:
   ```bash
   python step4_final_script_navigate_to_edit_pl_and_discount_lists_(dl).py
   ```
3. **Manual login**: you’ll be prompted to log in to Oracle Fusion manually before the script continues.

---

## ⚠️ About `step5` Scripts

The scripts `step5_navigate_to_edit_dl_and_currency_lists_(cl)_try1.py` and `try2.py` attempt to automate *Currency Conversion Lists*. However, Oracle Fusion displays a modal warning when the selected list is not approved, which **interrupts automation**. These scripts are not recommended for use until this limitation is resolved.

---

## 📌 Additional Notes

- All scripts use `WebDriverWait` and `ActionChains` for robust UI interaction.
- Dynamic scrolling and element visibility handling are included.
- Start dates are inserted automatically using the system’s current date.
- Start with one or two records to test before scaling up.

---

## 💡 FAQ

**Can I run the entire process with a single script?**  
Yes, `step4` is the most complete script for handling both Price and Discount Lists. Currency Lists are pending future support.

**What if I’m not using Chrome?**  
This setup depends on `webdriver-manager` for installing the correct ChromeDriver version. Chrome is required.

**Can the Currency Conversion List modal be bypassed?**  
No. This is a hard limitation of the Oracle Fusion production UI.

---

## ⚠️ Environment Recommendation

This tool uses Google Chrome and Selenium WebDriver with `webdriver-manager`, and **requires access to a local graphical browser**.

💡 We strongly recommend running this tool in a **local desktop environment** (Windows, macOS, or native Linux with Chrome installed), rather than in virtualized or headless environments like WSL, Docker, or CI/CD runners.

This ensures full compatibility with:
- Manual login steps required by Oracle Fusion
- UI interactions with popups, modals, and tab navigation
- Automatic ChromeDriver resolution

---