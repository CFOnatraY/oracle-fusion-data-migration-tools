import pandas as pd
import difflib
from unidecode import unidecode

# === Load files ===
input_file = "input_file.xlsx"
geography_file = "geography_report.xlsx"

input_df = pd.read_excel(input_file, dtype=str).fillna("")
geo_df = pd.read_excel(geography_file, dtype=str).fillna("")

# === Normalize base columns ===
for df in [input_df, geo_df]:
    for col in ["CITY", "STATE", "COUNTRY", "CHILD", "PARENT", "COUNTRY_CODE"]:
        if col in df.columns:
            df[col] = df[col].str.upper().str.strip()

# Rename for clarity
geo_df = geo_df.rename(columns={
    "COUNTRY_CODE": "COUNTRY",
    "PARENT": "STATE",
    "CHILD": "CITY"
})

# === Build valid geography triplets ===
valid_combinations = geo_df[["COUNTRY", "STATE", "CITY"]].drop_duplicates()
valid_combinations["is_valid"] = True
valid_combinations["matched_geography_path"] = (
    valid_combinations["COUNTRY"] + " > " +
    valid_combinations["STATE"] + " > " +
    valid_combinations["CITY"]
)

# === Compare exact matches ===
result_df = input_df.merge(
    valid_combinations,
    on=["COUNTRY", "STATE", "CITY"],
    how="left"
)

result_df["is_valid"] = result_df["is_valid"].fillna(False)
result_df["matched_geography_path"] = result_df["matched_geography_path"].fillna("NOT FOUND")

# === Add RIGHT_BLEND using fuzzy city match only for is_valid = False ===

# Prepare searchable geo data without tildes
geo_df["CITY_NORM"] = geo_df["CITY"].apply(unidecode)
geo_df["STATE_NORM"] = geo_df["STATE"].apply(unidecode)

def find_right_blend(row):
    if row["is_valid"]:
        return ""
    input_city_norm = unidecode(row["CITY"])
    input_country = row["COUNTRY"]
    
    possible = geo_df[geo_df["COUNTRY"] == input_country]
    matches = difflib.get_close_matches(input_city_norm, possible["CITY_NORM"], n=1, cutoff=0.8)
    
    if matches:
        matched_city = matches[0]
        match_row = possible[possible["CITY_NORM"] == matched_city].iloc[0]
        return f"{match_row['COUNTRY']} > {match_row['STATE']} > {match_row['CITY']}"
    return ""

# Apply to invalid rows
result_df["RIGHT_BLEND"] = result_df.apply(find_right_blend, axis=1)

# === Export
result_df.to_excel("geography_validation_with_right_blend.xlsx", index=False)
print("✅ RIGHT_BLEND con coincidencia aproximada generada correctamente.")
