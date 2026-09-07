import pandas as pd
from pathlib import Path

INPUT_PATH=Path(__file__).resolve().parents[2]/'data'/'raw'/'automotive_quality.csv'
df=pd.read_csv(INPUT_PATH)
print(f'loaded {len(df)} records!')
# print(df.isna().sum())

FAULT_CODES = {
    "Overheating": "BAT_TEMP",
    "Voltage Drop": "BAT_VOLT",
    "Cell Imbalance": "BAT_CELL",
    "Signal Error": "SIG_ERR",
    "Calibration Error": "CAL_ERR",
    "No Signal": "NO_SIG",
    "Invalid Reading": "TEMP_INV",
    "Signal Drift": "TEMP_DRIFT",
}
sev_type=['Low','Medium','High']
invalid_sev=~df['severity'].isin(sev_type)
duplicates=df.duplicated()

sensor_ranges={
    "Battery": (20, 80),
    "Brake Sensor": (0, 100),
    "Temperature Sensor": (-20, 120),
}

def has_invalid_value(n):
    min, max = sensor_ranges[n['component_type']]
    return not min<=n['sensor_value']<=max
invalid_values=df.apply(
    has_invalid_value,
    axis=1
)

quality_report = {
    "Total records": len(df),
    "Missing suppliers": df['supplier'].isna().sum(),
    "Missing fault codes": df['fault_code'].isna().sum(),
    "Invalid severities": invalid_sev.sum(),
    "Invalid sensor values": invalid_values.sum(),
    "Duplicate records": duplicates.sum(),
}

print("\nDATA QUALITY REPORT")
print("-------------------")

for issue, count in quality_report.items():
    print(f"{issue}: {count}")

def get_quality_issues(n):
    issues=[]
    if pd.isna(n['supplier']):
        issues.append('MISSING SUPPLIER')
    if pd.isna(n['fault_code']):
        issues.append('MISSING FAULT CODE')
    if n['severity'] not in sev_type:
        issues.append('INVALID SEVERITY')
    min, max= sensor_ranges[n['component_type']]
    if not min <=n['sensor_value'] <= max:
        issues.append('INVALID SENSOR VALUE')
    return issues

clean_df=df.copy()

df['quality_issues']=df.apply(get_quality_issues,axis=1)
df['quality_status']=df['quality_issues'].apply(
    lambda issue: 'VALID' if len(issue)==0 else 'INVALID'
)


for index in df[duplicates].index:
    df.at[index,'quality_issues'].append('DUPLICATE RECORD')
    df.at[index,'quality_stauts']='INVALID'

#data cleanup
clean_df=clean_df.drop_duplicates()
clean_df['supplier']=clean_df['supplier'].fillna('UNKNOWN')
clean_df['fault_code']=clean_df.apply(
    lambda n:FAULT_CODES.get(n['fault_type'])
    if pd.isna(n['fault_code']) else n['fault_code'],
    axis=1
)
clean_df.loc[
    ~clean_df['severity'].isin(sev_type),'severity'
]='UNKNOWN'

def sensor_vals(n):
    min,max = sensor_ranges[n['component_type']]
    if min<=n['sensor_value']<=max:
        return n['sensor_value']
    return pd.NA
clean_df['sensor_value']=clean_df.apply(sensor_vals,axis=1)
OUTPUT_PATH='data/processed/automotive_quality_clean.csv'
clean_df.to_csv(OUTPUT_PATH,index=False)
print('No of records after cleanup:',len(clean_df))