# Changelog: Ace Plumbing and HVAC (ACE_001)

**Version:** v1 → v2

**Date:** 2026-03-04T22:36:22.412223

**Summary:** Updated emergency routing to Mike as the sole contact, added Sunday hours, updated emergency definitions, and added new ServiceTrade constraints. Also updated the agent greeting and added a new special rule for new construction project estimates.

## Changes (9 field changes)

### `business_hours.days`
- **Before:** `Monday-Friday, Saturday`
- **After:** `Monday-Sunday`

### `call_transfer_rules.collect_before_transfer`
- **Added:** `['project type']`

### `emergency_definition`
- **Added:** `['gas smell']`

### `emergency_routing_rules.step_1.contact_name`
- **Before:** `Carlos`
- **After:** `Mike`

### `emergency_routing_rules.step_1.phone`
- **Before:** `512-555-0192`
- **After:** `512-555-0101`

### `integration_constraints`
- **Added:** `['do not create sprinkler jobs in ServiceTrade', 'do not create gas line estimates in ServiceTrade']`

### `integration_constraints`
- **Removed:** `['do not create sprinkler or fire suppression jobs in ServiceTrade']`

### `special_rules`
- **Added:** `["If someone specifically asks for an estimate for a new construction project, take their info and tell them we'll have our estimator, Paula, call them back."]`

### `v1_to_v2_changes`
- **Added:** `{'added': ['Sunday hours', 'new ServiceTrade constraint: do not create gas line estimates', 'new special rule: new construction project estimates', 'new greeting: Ace Plumbing and HVAC, serving Austin since 1998'], 'updated': ['emergency routing rules', 'emergency definitions', 'integration constraints', 'greeting', 'special rules'], 'removed': ['Carlos as emergency contact', 'step_2 in emergency routing rules', "collect_before_transfer: what it's about"]}`

## New Rules Added
- If someone specifically asks for an estimate for a new construction project, take their info and tell them we'll have our estimator, Paula, call them back.

## Agent System Prompt
- ✅ Updated to reflect all v2 changes

