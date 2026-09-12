import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

NEO4J_URI=os.getenv('NEO4J_URI')
NEO4J_USERNAME=os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD=os.getenv('NEO4J_PASSWORD')

def get_battery_overheating_stats():
    query="""
    MATCH (i:Inspection)-[:SUPPLIER]->(s:Supplier),
          (i)-[:INSPECTED_COMPONENT]->(c:Component)
    WHERE c.component_type = "Battery"

    WITH s, count(i) AS total_battery_inspections

    MATCH (i2:Inspection)-[:SUPPLIER]->(s),
          (i2)-[:INSPECTED_COMPONENT]->(c2:Component),
          (i2)-[:DETECTED_FAULT]->(f:Fault)
    WHERE c2.component_type = "Battery"
      AND f.fault_type = "Overheating"

    RETURN
        s.name AS supplier,
        total_battery_inspections,
        count(i2) AS overheating_cases,
        round(
            100.0 * count(i2) / total_battery_inspections,
            2
        ) AS overheating_rate

    ORDER BY overheating_rate DESC
    """
    driver=GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USERNAME,NEO4J_PASSWORD)
    )
    try:
        with driver.session() as session:
            results=session.run(query)
            records=[]
            for record in results:
                records.append({
                    'supplier':record['supplier'],
                    'total_battery_inspections':record['total_battery_inspections'],
                    'overheating_cases':record['overheating_cases'],
                    'overheating_rate':record['overheating_rate']
                })
            return records
    finally:
        driver.close()
if __name__=='__main__':
    stats=get_battery_overheating_stats()
    for item in stats:
        print(item)