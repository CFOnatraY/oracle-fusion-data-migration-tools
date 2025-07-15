import pandas as pd

# === Load files ===
input_file = "input_file.xlsx"
geography_file = "geography_file.xlsx"

input_df = pd.read_excel(input_file, dtype=str).fillna("")
geography_df = pd.read_excel(geography_file, dtype=str).fillna("")

# === Normalize columns ===
input_df["COUNTRY"] = input_df["COUNTRY"].str.upper().str.strip()
input_df["STATE"] = input_df["STATE"].str.upper().str.strip()
input_df["CITY"] = input_df["CITY"].str.upper().str.strip()
geography_df["PrimaryGeographyName"] = geography_df["PrimaryGeographyName"].str.upper().str.strip()
geography_df["CountryCode"] = geography_df["CountryCode"].str.upper().str.strip()

# === Split levels ===
level_1 = geography_df[geography_df["LevelNumber"] == "1"].rename(columns={
    "PrimaryGeographyName": "CountryName",
    "SourceId": "CountryId"
})
level_2 = geography_df[geography_df["LevelNumber"] == "2"].rename(columns={
    "PrimaryGeographyName": "StateName",
    "SourceId": "StateId",
    "ParentSourceId": "CountryId"
})
level_3 = geography_df[geography_df["LevelNumber"] == "3"].rename(columns={
    "PrimaryGeographyName": "CityName",
    "ParentSourceId": "StateId"
})

# === Merge hierarchy to get valid triplets ===
merged_city_state = level_3.merge(level_2, on="StateId", how="left")
merged_full = merged_city_state.merge(level_1, on="CountryId", how="left")

valid_combinations = merged_full[["CountryCode", "StateName", "CityName"]].copy()
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

result_df["is_valid"] = result_df["is_valid"].fillna(False)
result_df["matched_geography_path"] = result_df["matched_geography_path"].fillna("NOT FOUND")

# === Export result ===
result_df.to_excel("geography_validation_result.xlsx", index=False)
print("✅ Comparison complete. Results saved to 'geography_validation_result.xlsx'")
