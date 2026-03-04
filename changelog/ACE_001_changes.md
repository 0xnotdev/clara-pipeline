# Changelog: Ace Plumbing and HVAC (ACE_001)

**Version:** v1 → v2

**Date:** 2026-03-04T12:01:29.734691

**Summary:** Updated emergency routing to Mike as the sole contact, added Sunday hours, updated emergency definitions, and added new ServiceTrade constraints and routing rules.

## Changes (13 field changes)

### `after_hours_flow_summary`
- **Before:** `Emergency calls are routed to Carlos then Mike, non-emergency calls are messaged and returned the next morning`
- **After:** `Emergency calls are routed to Mike, non-emergency calls are messaged and returned the next morning`

### `business_hours.days`
- **Before:** `Monday-Friday, Saturday`
- **After:** `Monday-Sunday`

### `call_transfer_rules.if_no_answer`
- **Before:** `None`
- **After:** `take their info and tell them we'll have our estimator, Paula, call them back`

### `emergency_definition`
- **Added:** `['gas smell']`

### `emergency_routing_rules.step_1.contact_name`
- **Before:** `Carlos`
- **After:** `Mike`

### `emergency_routing_rules.step_1.phone`
- **Before:** `512-555-0192`
- **After:** `512-555-0101`

### `greeting_update`
- **Added:** `Ace Plumbing and HVAC, serving Austin since 1998`

### `integration_constraints`
- **Added:** `['do not create sprinkler jobs in ServiceTrade', 'do not create gas line estimates in ServiceTrade']`

### `integration_constraints`
- **Removed:** `['do not create sprinkler or fire suppression jobs in ServiceTrade']`

### `new_rules_added`
- **Added:** `["If someone specifically asks for an estimate for a new construction project, take their info and tell them we'll have our estimator, Paula, call them back."]`

### `special_rules_updates`
- **Added:** `['escalate to Mike directly if caller is upset or threatening']`

### `summary`
- **Added:** `Updated emergency routing to Mike as the sole contact, added Sunday hours, updated emergency definitions, and added new ServiceTrade constraints and routing rules.`

### `v1_to_v2_changes`
- **Added:** `{'emergency_routing_rules': 'Updated emergency routing to Mike as the sole contact', 'business_hours': 'Added Sunday hours', 'emergency_definition': "Added 'gas smell' to emergency definition list", 'integration_constraints': 'Added constraint to never create gas line estimates in ServiceTrade', 'call_transfer_rules': 'Added new routing rule for new construction project estimates'}`

## New Rules Added
- If someone specifically asks for an estimate for a new construction project, take their info and tell them we'll have our estimator, Paula, call them back.

## Agent System Prompt
- ✅ Updated to reflect all v2 changes

