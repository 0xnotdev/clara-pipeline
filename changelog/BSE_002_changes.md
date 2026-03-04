# Changelog: Bright Star Electrical (BSE_002)

**Version:** v1 → v2

**Date:** 2026-03-04T22:37:11.029823

**Summary:** Updated office hours, emergency routing rules, emergency definitions, integration constraints, and agent greeting. Added new VIP client for Lakewood General.

## Changes (11 field changes)

### `business_hours.days`
- **Before:** `Monday-Friday`
- **After:** `Monday-Thursday, 8:00 AM - 5:00 PM, Friday, 8:00 AM - 4:30 PM`

### `emergency_definition`
- **Removed:** `['Power outage affecting the whole property', 'Exposed or sparking wires', 'Electrical fire smell', 'Panel issues that cut power to critical equipment']`

### `emergency_definitions`
- **Added:** `['Power outage affecting the whole property', 'Exposed or sparking wires', 'Electrical fire smell', 'Panel issues that cut power to critical equipment', 'Generator failure at a medical facility']`

### `emergency_routing_rules.fallback`
- **Before:** `Tell the caller a tech will call back within 30 minutes and page Dave via the internal system`
- **After:** `Same as before`

### `emergency_routing_rules.step_1.phone`
- **Before:** `720-555-0344`
- **After:** `720-555-0399`

### `emergency_routing_rules.step_2.phone`
- **Before:** `720-555-0300`
- **After:** `720-555-0355`

### `emergency_routing_rules.step_2.rings_before_next`
- **Before:** `None`
- **After:** `3`

### `greeting`
- **Added:** `Bright Star Electrical, licensed and insured in Colorado`

### `integration_constraints`
- **Added:** `['Note permit work prominently']`

### `special_rules`
- **Added:** `['VIP client: Lakewood General, escalate immediately to Sandra']`

### `v1_to_v2_changes`
- **Added:** `[{'field': 'business_hours', 'old_value': 'Monday-Friday, 8:00 AM - 5:00 PM', 'new_value': 'Monday-Thursday, 8:00 AM - 5:00 PM, Friday, 8:00 AM - 4:30 PM', 'reason': 'Office hours updated to reflect new closing time on Fridays'}, {'field': 'emergency_routing_rules.step_1.phone', 'old_value': '720-555-0344', 'new_value': '720-555-0399', 'reason': "Dave Kowalski's phone number changed"}, {'field': 'emergency_routing_rules.step_2.phone', 'old_value': None, 'new_value': '720-555-0355', 'reason': 'New backup contact added'}, {'field': 'emergency_routing_rules.step_2.rings_before_next', 'old_value': None, 'new_value': 3, 'reason': 'New backup contact added'}, {'field': 'emergency_definitions', 'old_value': ['Power outage affecting the whole property', 'Exposed or sparking wires', 'Electrical fire smell', 'Panel issues that cut power to critical equipment'], 'new_value': ['Power outage affecting the whole property', 'Exposed or sparking wires', 'Electrical fire smell', 'Panel issues that cut power to critical equipment', 'Generator failure at a medical facility'], 'reason': 'New emergency definition added'}, {'field': 'integration_constraints', 'old_value': ['Jobber field management platform', 'Do not create or cancel jobs'], 'new_value': ['Jobber field management platform', 'Do not create or cancel jobs', 'Note permit work prominently'], 'reason': 'New constraint added'}, {'field': 'greeting', 'old_value': None, 'new_value': 'Bright Star Electrical, licensed and insured in Colorado', 'reason': 'New agent greeting added'}, {'field': 'special_rules', 'old_value': ['VIP client: Denver Metro Hospital, escalate immediately to Sandra at 720-555-0411'], 'new_value': ['VIP client: Denver Metro Hospital, escalate immediately to Sandra at 720-555-0411', 'VIP client: Lakewood General, escalate immediately to Sandra'], 'reason': 'New VIP client added'}]`

## Agent System Prompt
- ✅ Updated to reflect all v2 changes

