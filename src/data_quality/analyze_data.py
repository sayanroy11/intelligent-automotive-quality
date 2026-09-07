import pandas as pd
from pathlib import Path
path=Path(__file__).resolve().parents[2]/'data'/'processed'/'automotive_quality_clean.csv'
df=pd.read_csv(path)
print(f'Loaded {len(df)} records')

battery_df=df[df['component_type']=='Battery']
# print(battery_df['fault_type'].value_counts())
supplierfault=pd.crosstab(
    battery_df['supplier'],battery_df['fault_type']
)
# print('Battery fault by suppliers:')
# print(supplierfault)

overheating_rate=(
    battery_df.assign(is_overheating=battery_df['fault_type']=='Overheating')
    .groupby('supplier')['is_overheating']
    .mean()
    .mul(100)
    .round(2)
)
print('Battery overheating rate by supplier:')
print(overheating_rate)
