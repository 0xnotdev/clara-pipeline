# Changelog: Nordic HVAC Solutions (NHS_004)

**Version:** v1 → v2

**Date:** 2026-03-04T22:38:34.078885

**Summary:** Extended business hours, updated emergency routing rules, added new emergency trigger, and new integration constraints. Also updated greeting text and added VIP account escalation rule.

## Changes (8 field changes)

### `business_hours.days`
- **Before:** `Monday-Friday`
- **After:** `Monday-Friday, Saturday`

### `business_hours.end`
- **Before:** `6:00 PM`
- **After:** `['6:00 PM', '4:00 PM']`

### `call_transfer_rules.office_hours_transfer_to`
- **Before:** `Main Office 612-555-0100`
- **After:** `Nordic HVAC Solutions, commercial comfort specialists`

### `emergency_definition`
- **Added:** `['HVAC failure in a data center']`

### `emergency_routing_rules.step_1.callback_guarantee`
- **Added:** `{'medical_facilities_and_server_rooms': '30 minutes', 'all_others': '60 minutes'}`

### `integration_constraints`
- **Added:** `['Do not quote prices to callers']`

### `special_rules`
- **Added:** `[{'caller_id': "North Memorial Health or Children's Minnesota", 'escalation_contact': 'Ingrid Halvorsen, 612-555-0200'}]`

### `v1_to_v2_changes`
- **Added:** `{'added': ['HVAC failure in a data center as emergency trigger', 'Do not quote prices to callers', 'Nordic HVAC Solutions, commercial comfort specialists', "North Memorial Health or Children's Minnesota as VIP accounts"], 'updated': ['business hours', 'emergency routing rules', 'emergency definition', 'integration constraints', 'greeting text', 'special rules']}`

## New Rules Added
- HVAC failure in a data center as emergency trigger

## Agent System Prompt
- ✅ Updated to reflect all v2 changes

