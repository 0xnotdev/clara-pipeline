# Changelog: Gulf Coast Roofing (GCR_003)

**Version:** v1 → v2

**Date:** 2026-03-04T12:02:50.499699

**Summary:** Gulf Coast Roofing updated their business hours, emergency contact, and special rules, including a new VIP rule for hurricane damage.

## Changes (6 field changes)

### `business_hours.end`
- **Before:** `7:00 PM`
- **After:** `5:00 PM`

### `emergency_definition`
- **Added:** `['tarp fell off a previously damaged roof']`

### `emergency_routing_rules.step_1.phone`
- **Before:** `713-555-0277`
- **After:** `713-555-0310`

### `greeting_update`
- **Added:** `Gulf Coast Roofing, Houston's trusted roofers`

### `special_rules`
- **Added:** `['Hurricane damage goes to storm division']`

### `v1_to_v2_changes`
- **Added:** `{'business_hours': {'old_value': {'end': '7:00 PM'}, 'new_value': {'end': '5:00 PM'}, 'reason': 'Tony Marchand mentioned they cut back Saturday hours'}, 'emergency_routing_rules.step_1.phone': {'old_value': '713-555-0277', 'new_value': '713-555-0310', 'reason': 'Ray got promoted and Marcus is the new emergency contact'}, 'emergency_definition': {'old_value': None, 'new_value': 'tarp fell off a previously damaged roof', 'reason': 'Tony Marchand added a new emergency definition'}, 'call_transfer_rules.collect_before_transfer': {'old_value': None, 'new_value': 'Residential or Commercial', 'reason': 'Tony Marchand wanted the agent to always ask about residential or commercial property'}, 'special_rules': {'old_value': 'Flag insurance claims for separate follow-up', 'new_value': 'Flag insurance claims for separate follow-up, Hurricane damage goes to storm division', 'reason': 'Tony Marchand added a new VIP rule for hurricane damage'}}`

## New Rules Added
- Hurricane damage goes to storm division

## Agent System Prompt
- ✅ Updated to reflect all v2 changes

