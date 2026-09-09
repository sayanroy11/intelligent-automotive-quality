// overheating cases by supplier
MATCH(i:Inspection)-(:SUPPLIER)->(s.Supplier),
     (i)-[:DETECTED_FAULT]->(f:Fault)
WHERE f.fault_type = "Overheating"
RETURN s.name as supplier,
       count(*) as overheating_cases
ORDER BY overheating_cases DESC;

//Overheating rate by supplier
MATCH (i:Inspection)-[:SUPPLIER]->(s:Supplier),
      (i)-[:INSPECTED_COMPONENT]->(c:Component)
WHERE c.component_type = "Battery"
WITH s, count(i) AS total_battery_inspections
MATCH (i2:Inspection)-[:SUPPLIER]->(s),
      (i2)-[:INSPECTED_COMPONENT]->(c2:Component),
      (i2)-[:DETECTED_FAULT]->(f:Fault)
WHERE c2.component_type = "Battery"
  AND f.fault_type = "Overheating"
RETURN s.name AS supplier,
       total_battery_inspections,
       count(i2) AS overheating_cases,
       round(
           100.0 * count(i2) / total_battery_inspections,
           2
       ) AS overheating_rate
ORDER BY overheating_rate DESC;

//Fault severity distribution
MATCH(i:Inspection)-[:DETECTED_FAULT]->(f:Fault)
RETURN f.fault_type AS fault,
       i.severity AS severity,
       count(*) as cases
ORDER BY fault,cases DESC;


//Investigate one supplier
MATCH (i:Inspection)-[:SUPPLIER]->(s:Supplier),
      (i)-[:INSPECTED_COMPONENT]->(c:Component),
      (i)-[:DETECTED_FAULT]->(f:Fault)
WHERE s.name = "Supplier_B"

RETURN c.component_type AS component,
       f.fault_type AS fault,
       count(*) AS cases
ORDER BY cases DESC;