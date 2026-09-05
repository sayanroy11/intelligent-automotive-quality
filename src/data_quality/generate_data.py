import random
from datetime import datetime,timedelta
import numpy as np
import pandas as pd

NUM_RECORDS=2000
RANDOM_SEED=1
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

MODELS=["MODEL_A","MODEL_B","MODEL_C"]
PLANTS=["Plant_1","Plant_2","Plant_3"]
COMPONENTS={
    "Battery":{
        "faults":['Overheating','Voltage Drop','Cell Imbalance'],
        "sensor_range":(20,80),
    },
    "Brake Sensor":{
        "faults":['Signal Error','Calibration Error','No Signal'],
        "sensor_range":(0,100),
    },
    "Temperature Sensor":{
        "faults":['Invalid Reading','Signal Drift','No Signal'],
        "sensor_range":(-20,120)
    }
}
SUPPLIERS=['Supplier_A','Supplier_B','Supplier_C']

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

def generate_inspection(index):
    component_type=random.choice(list(COMPONENTS.keys()))
    supplier=random.choice(SUPPLIERS)
    possible_faults=COMPONENTS[component_type]["faults"]
    fault_type=random.choice(possible_faults)
    if component_type=="Battery" and supplier=='Supplier_B':
        if random.random() < 0.5:
            fault_type='Overheating'
    sensor_min,sensor_max=COMPONENTS[component_type]['sensor_range']
    sensor_value=round(random.uniform(sensor_min,sensor_max),2)
    inspection_date=datetime(2026,1,1)+timedelta(days=random.randint(0,240))
    severity=random.choice(['Low','Medium','High'])
    inspection_result='Fail'

    repair_actions = {
        "Overheating": "Inspect cooling system",
        "Voltage Drop": "Check battery voltage",
        "Cell Imbalance": "Inspect battery cells",
        "Signal Error": "Inspect sensor connection",
        "Calibration Error": "Recalibrate sensor",
        "No Signal": "Check wiring and connector",
        "Invalid Reading": "Replace or recalibrate sensor",
        "Signal Drift": "Perform sensor calibration",
    }
    return {
        "inspection_id": f"INS{index:04d}",
        "vehicle_id": f"V{random.randint(1, 500):04d}",
        "model": random.choice(MODELS),
        "plant": random.choice(PLANTS),
        "component_id": f"CMP{random.randint(1, 300):04d}",
        "component_type": component_type,
        "supplier": supplier,
        "inspection_date": inspection_date.date(),
        "fault_code": FAULT_CODES[fault_type],
        "fault_type": fault_type,
        "severity": severity,
        "sensor_value": sensor_value,
        "inspection_result": inspection_result,
        "repair_action": repair_actions[fault_type],
    }

records=[]
for i in range(1,NUM_RECORDS+1):
    records.append(generate_inspection(i))
df=pd.DataFrame(records)
#print(df.head())


# injecting data-quality issues.
missing_supp_id=np.random.choice(
    df.index,
    size=int(0.02*len(df)),
    replace=False
)
df.loc[missing_supp_id,'supplier']=np.nan

severity_idx=np.random.choice(
    df.index,
    size=int(0.01*len(df)),
    replace=False
)
df.loc[severity_idx,'severity']='Critical'

sensor_idx=np.random.choice(
    df.index,
    size=int(0.01*len(df)),
    replace=False
)
df.loc[sensor_idx,'sensor_value']=9999

fault_code_idx=np.random.choice(
    df.index,
    size=int(0.01*len(df)),
    replace=False
)
df.loc[fault_code_idx,'fault_code']=np.nan

duplicate_rows=df.sample(
    n=int(0.01*len(df)),
    random_state=RANDOM_SEED
)
df=pd.concat([df,duplicate_rows],ignore_index=True)
output_path="data/raw/automotive_quality.csv"
df.to_csv(output_path,index=False)
print('Total records!:',len(df))