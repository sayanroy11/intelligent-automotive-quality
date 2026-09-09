import os
import pandas as pd
from dotenv import load_dotenv
from neo4j import GraphDatabase
from pathlib import Path

load_dotenv()
URI=os.getenv('NEO4J_URI')
USERNAME=os.getenv('NEO4J_USERNAME')
PASSWORD=os.getenv('NEO4J_PASSWORD')

DATA_PATH=Path(__file__).resolve().parents[2]/'data'/'processed'/'automotive_quality_clean.csv'
driver=GraphDatabase.driver(
    URI,
    auth=(USERNAME,PASSWORD)
    )
print('Connected to Neo4j!')
df=pd.read_csv(DATA_PATH)
print(f'Loaded {len(df)} records')

def create_inspection(tx,row):
    query="""
    MERGE (v: Vehicle {vehicle_id: $vehicle_id})
    SET v.model=$model,
        v.plant=$plant
    
    MERGE (i:Inspection {inspection_id: $inspection_id})
    SET i.inspection_date=$inspection_date,
        i.sensor_value=$sensor_value,
        i.inspection_result=$inspection_result,
        i.severity=$severity 
        
    MERGE (c: Component {componet_id: $component_id})
    SET c.component_type=$component_type
    
    MERGE (s:Supplier {name: $supplier})
    
    MERGE (f:Fault {fault_code: $fault_code})
    SET f.fault_type= $fault_type
    
    MERGE(r:RepairAction {name: $repair_action})
    
    MERGE (v)-[:HAS_INSPECTION]->(i)
    MERGE (i)-[:INSPECTED_COMPONENT]->(c)
    MERGE (i)-[:SUPPLIER]->(s)
    MERGE (i)-[:DETECTED_FAULT]->(f)
    MERGE (i)-[:RECOMMENDS_ACTION]->(r)
    """
    tx.run(
        query,
        vehicle_id=row["vehicle_id"],
        model=row["model"],
        plant=row["plant"],
        inspection_id=row["inspection_id"],
        inspection_date=row["inspection_date"],
        sensor_value=row["sensor_value"],
        inspection_result=row["inspection_result"],
        severity=row["severity"],
        component_id=row["component_id"],
        component_type=row["component_type"],
        supplier=row["supplier"],
        fault_code=row["fault_code"],
        fault_type=row["fault_type"],
        repair_action=row["repair_action"],
    )

with driver.session() as session:
      for _,row in df.iterrows():
        session.execute_write(
            create_inspection,
            row
        )
driver.close()
print(f'Added {len(df)} records to neo4j!')