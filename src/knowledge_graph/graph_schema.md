## Nodes

### Vehicle
Properties:
- vehicle_id
- model
- plant
### Inspection
Properties:
- inspection_id
- inspection_date
- sensor_value
- inspection_result
- severity
### Component
Properties:
- component_id
- component_type
### Supplier
Properties:
- name
### Fault
Properties:
- fault_code
- fault_type
### RepairAction
Properties:
- name
## Relationships
- vehicle -[:HAS_INSPECTION]->Inspection
- Inspection -[:INSPECTED_COMPONENT]->Component
- Inspection -[:SUPPLIER]->Supplier
- Inspection -[:DETECTED_FAULT]->Fault
- Inspection - [:RECOMMENDS_ACTION]->RepairAction