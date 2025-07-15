import pandas as pd

# === Load files ===
input_file = "input_file.xlsx"
converted_report_file = "geography_report.xlsx"

input_df = pd.read_excel(input_file, dtype=str).fillna("")
geo_df = pd.read_excel(converted_report_file, dtype=str).fillna("")

# === Normalize columns ===
input_df["COUNTRY"] = input_df["COUNTRY"].str.upper().str.strip()
input_df["STATE"] = input_df["STATE"].str.upper().str.strip()
input_df["CITY"] = input_df["CITY"].str.upper().str.strip()

geo_df["COUNTRY_CODE"] = geo_df["COUNTRY_CODE"].str.upper().str.strip()
geo_df["PARENT"] = geo_df["PARENT"].str.upper().str.strip()  # State
geo_df["CHILD"] = geo_df["CHILD"].str.upper().str.strip()    # City

# === Build valid triplets ===
valid_combinations = geo_df[["COUNTRY_CODE", "PARENT", "CHILD"]].copy()
valid_combinations.columns = ["COUNTRY", "STATE", "CITY"]
valid_combinations["is_valid"] = True
valid_combinations["matched_geography_path"] = (
    valid_combinations["COUNTRY"] + " > " +
    valid_combinations["STATE"] + " > " +
    valid_combinations["CITY"]
)

# === Compare input file against valid triplets ===
result_df = input_df.merge(
    valid_combinations,
    on=["COUNTRY", "STATE", "CITY"],
    how="left"
)

# === Finalize result
result_df["is_valid"] = result_df["is_valid"].fillna(False)
result_df["matched_geography_path"] = result_df["matched_geography_path"].fillna("NOT FOUND")

# === Export to Excel
result_df.to_excel("geography_validation_result_v2.xlsx", index=False)
print("✅ Comparison complete. Results saved to 'geography_validation_result_v2.xlsx'")
