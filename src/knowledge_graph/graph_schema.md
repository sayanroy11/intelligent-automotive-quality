## Nodes

### Vehicle
Properties:
- vehicle_id
- model
- plant

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
- severity
### RepairAction
Properties:
- name
## Relationships
- vehicle -[:HAS_COMPONENT]->Component
- Component -[:SUPPLIED_BY]->Supplier
- Component -[:HAS_FAULT]->Fault
- Fault - [:RESOLVED_BY]->RepairAction