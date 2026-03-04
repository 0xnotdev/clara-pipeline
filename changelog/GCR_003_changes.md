# Changelog: Gulf Coast Roofing (GCR_003)

**Version:** v1 → v2

**Date:** 2026-03-04T22:37:51.990783

**Summary:** Gulf Coast Roofing updated their business hours, emergency contact, emergency definitions, and added new rules for residential/commercial properties and hurricane damage. They also updated their greeting and added a new VIP rule.

## Changes (7 field changes)

### `business_hours.end`
- **Before:** `7:00 PM`
- **After:** `5:00 PM`

### `emergency_definition`
- **Added:** `['tarp fell off a previously damaged roof']`

### `emergency_routing_rules.step_1.phone`
- **Before:** `713-555-0277`
- **After:** `713-555-0310`

### `greeting`
- **Added:** `Gulf Coast Roofing, Houston's trusted roofers`

### `new_rules_added`
- **Added:** `['is this for a residential or commercial property? Always. Every call.', 'if they mention hurricane damage specifically, that goes to our storm division']`

### `special_rules`
- **Added:** `['is this for a residential or commercial property? Always. Every call.', 'if they mention hurricane damage specifically, that goes to our storm division']`

### `v1_to_v2_changes`
- **Added:** `{'business_hours': {'old_value': '7:00 PM', 'new_value': '5:00 PM', 'reason': 'Tony Marchand mentioned they cut back Saturday hours'}, 'emergency_routing_rules.step_1.phone': {'old_value': '713-555-0277', 'new_value': '713-555-0310', 'reason': 'Ray got promoted and Marcus is the new emergency contact'}, 'emergency_definition': {'old_value': 'null', 'new_value': 'tarp fell off a previously damaged roof', 'reason': 'Tony Marchand added a new emergency definition'}, 'call_transfer_rules.collect_before_transfer': {'old_value': 'null', 'new_value': 'Residential or Commercial', 'reason': 'Tony Marchand wanted the agent to always ask about residential or commercial property'}, 'special_rules': {'old_value': 'null', 'new_value': 'if they mention hurricane damage specifically, that goes to our storm division', 'reason': 'Tony Marchand added a new VIP rule'}}`

## New Rules Added
- is this for a residential or commercial property? Always. Every call.
- if they mention hurricane damage specifically, that goes to our storm division

## Agent System Prompt
- ✅ Updated to reflect all v2 changes

