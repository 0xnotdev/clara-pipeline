# Changelog: Rapid Response Restoration (RRR_005)

**Version:** v1 → v2

**Date:** 2026-03-04T22:39:17.699162

**Summary:** Rapid Response Restoration expanded to serve Charlotte, NC, and updated emergency routing, definitions, and special rules to accommodate the new market and services.

## Changes (8 field changes)

### `emergency_definition`
- **Added:** `['biohazard cleanup requests']`

### `emergency_routing_rules.step_1.phone`
- **Before:** `404-555-0600`
- **After:** `404-555-0600 (Atlanta) or 704-555-0700 (Charlotte)`

### `greeting`
- **Added:** `Rapid Response Restoration, serving Atlanta and Charlotte.`

### `integration_constraints`
- **Added:** `['Encircle']`

### `new_rules_added`
- **Added:** `['Ask for city and zip code early in the call to determine market', 'If caller says FEMA or federal disaster declaration, escalate to Jerome directly', 'If caller says property is vacant or abandoned, flag as different liability situation']`

### `office_address`
- **Before:** `3200 Peachtree Road NE, Atlanta GA 30305`
- **After:** `Expanded to serve Charlotte, NC`

### `special_rules`
- **Added:** `['flag if property is vacant or abandoned']`

### `v1_to_v2_changes`
- **Added:** `{'office_address': 'Expanded to serve Charlotte, NC', 'emergency_routing_rules.step_1.phone': '404-555-0600 (Atlanta) or 704-555-0700 (Charlotte)', 'emergency_definition': ['biohazard cleanup requests'], 'integration_constraints': ['Encircle'], 'special_rules': ['flag if property is vacant or abandoned'], 'greeting': 'Rapid Response Restoration, serving Atlanta and Charlotte.', 'summary': 'Rapid Response Restoration expanded to serve Charlotte, NC, and updated emergency routing, definitions, and special rules to accommodate the new market and services.'}`

## New Rules Added
- Ask for city and zip code early in the call to determine market
- If caller says FEMA or federal disaster declaration, escalate to Jerome directly
- If caller says property is vacant or abandoned, flag as different liability situation

## Agent System Prompt
- ✅ Updated to reflect all v2 changes

