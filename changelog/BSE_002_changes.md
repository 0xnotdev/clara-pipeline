# Changelog: Bright Star Electrical (BSE_002)

**Version:** v1 → v2

**Date:** 2026-03-04T12:02:10.400592

**Summary:** Updated office hours, emergency routing rules, and special rules to reflect changes in business operations and client relationships.

## Changes (12 field changes)

### `after_hours_flow_summary`
- **Before:** `Emergency calls are handled according to the emergency routing rules`
- **After:** `Emergency calls are handled according to the emergency routing rules, with new contacts and rules`

### `business_hours.end`
- **Before:** `5:00 PM`
- **After:** `4:30 PM`

### `emergency_definition`
- **Added:** `['generator failure at a medical facility']`

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
- **Added:** `['Cannot create or cancel jobs, note permit work prominently']`

### `integration_constraints`
- **Removed:** `['Cannot create or cancel jobs']`

### `office_hours_flow_summary`
- **Before:** `Collect information and transfer to the front desk`
- **After:** `Collect information and transfer to the front desk, with updated office hours`

### `special_rules`
- **Added:** `['VIP client: Lakewood General, escalate immediately to Sandra']`

### `v1_to_v2_changes`
- **Added:** `{'business_hours': {'end': '4:30 PM'}, 'emergency_routing_rules': {'step_1': {'phone': '720-555-0399'}, 'step_2': {'phone': '720-555-0355', 'rings_before_next': 3}}, 'emergency_definition': ['generator failure at a medical facility'], 'integration_constraints': ['Cannot create or cancel jobs, note permit work prominently'], 'after_hours_flow_summary': 'Emergency calls are handled according to the emergency routing rules, with new contacts and rules', 'office_hours_flow_summary': 'Collect information and transfer to the front desk, with updated office hours', 'special_rules': ['VIP client: Lakewood General, escalate immediately to Sandra']}`

## Agent System Prompt
- ✅ Updated to reflect all v2 changes

