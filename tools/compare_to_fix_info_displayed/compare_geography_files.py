import pandas as pd

# === Load Excel files ===
rollout_file = 'rollout_file.xlsx'
geo_file = 'geography_file.xlsx'

# Load and normalize
rollout_df = pd.read_excel(rollout_file, dtype=str).fillna('')
geo_df = pd.read_excel(geo_file, dtype=str).fillna('')

# Define keys and columns to compare
key_columns = ['SourceId', 'ParentSourceId', 'LevelNumber']
compare_columns = ['PrimaryGeographyName', 'CountryCode', 'RecordTypeCode']

# Normalize all values
for df in [rollout_df, geo_df]:
    for col in key_columns + compare_columns:
        df[col] = df[col].str.upper().str.strip()

# === Detect duplicates ===
rollout_duplicates = rollout_df[rollout_df.duplicated(subset=key_columns, keep=False)]
geo_duplicates = geo_df[geo_df.duplicated(subset=key_columns, keep=False)]

# === Merge for direct comparison ===
comparison_df = rollout_df.merge(
    geo_df,
    on=key_columns,
    how='left',
    suffixes=('_rollout', '_geo'),
    indicator=True
)

# === Mismatches
diff_records = []
match_counts = {col: 0 for col in compare_columns}

for _, row in comparison_df.iterrows():
    if row['_merge'] == 'left_only':
        diff_records.append({
            'SourceId': row['SourceId'],
            'ParentSourceId': row['ParentSourceId'],
            'LevelNumber': row['LevelNumber'],
            'PrimaryGeographyName_rollout': row.get('PrimaryGeographyName_rollout', ''),
            'Issue': 'Missing in geografia_cvj_co'
        })
        continue

    # Check for column mismatches
    issues = []
    for col in compare_columns:
        rollout_val = row[f'{col}_rollout']
        geo_val = row[f'{col}_geo']
        if rollout_val != geo_val:
            issues.append(f"{col} mismatch (Rollout: '{rollout_val}' vs Geo: '{geo_val}')")
        else:
            match_counts[col] += 1

    if issues:
        diff_records.append({
            'SourceId': row['SourceId'],
            'ParentSourceId': row['ParentSourceId'],
            'LevelNumber': row['LevelNumber'],
            'PrimaryGeographyName_rollout': row['PrimaryGeographyName_rollout'],
            'Issue': "; ".join(issues)
        })
    else:
        for col in compare_columns:
            match_counts[col] += 1  # Perfect match

# === Reverse missing check (Geo not in Rollout)
reverse_df = geo_df.merge(
    rollout_df,
    on=key_columns,
    how='left',
    indicator=True
)
missing_in_rollout = reverse_df[reverse_df['_merge'] == 'left_only'].drop(columns=['_merge'])

# === Summary stats
summary = {
    'Total Records in Rollout': len(rollout_df),
    'Total Records in Geography': len(geo_df),
    'Total Duplicates in Rollout': len(rollout_duplicates),
    'Total Duplicates in Geography': len(geo_duplicates),
    'Total Differences Found': len(diff_records),
    'Missing Records in Rollout': len(missing_in_rollout),
}

for col in compare_columns:
    summary[f'{col} Match Count'] = match_counts[col]
    summary[f'{col} Match %'] = round(match_counts[col] / len(rollout_df) * 100, 2) if len(rollout_df) else 0

summary_df = pd.DataFrame([summary])

# === Save to Excel
with pd.ExcelWriter('geography_comparison_result.xlsx', engine='openpyxl') as writer:
    pd.DataFrame(diff_records).to_excel(writer, sheet_name='Differences', index=False)
    rollout_duplicates.to_excel(writer, sheet_name='Rollout Duplicates', index=False)
    geo_duplicates.to_excel(writer, sheet_name='Geography Duplicates', index=False)
    missing_in_rollout.to_excel(writer, sheet_name='Missing in Rollout', index=False)
    summary_df.to_excel(writer, sheet_name='Summary', index=False)

print("✅ Full audit comparison complete.")
print("📊 Output written to 'geography_comparison_result.xlsx'")
