# Changelog: Rapid Response Restoration (RRR_005)

**Version:** v1 → v2

**Date:** 2026-03-04T12:04:22.959154

**Summary:** Rapid Response Restoration expanded its service area to include Charlotte, NC, and updated its emergency routing rules, special rules, and greeting to reflect this change.

## Changes (8 field changes)

### `emergency_definition`
- **Added:** `['biohazard cleanup requests']`

### `emergency_routing_rules.step_1.contact_name`
- **Before:** `dispatch`
- **After:** `dispatch (Atlanta) or Charlotte dispatch`

### `emergency_routing_rules.step_1.phone`
- **Before:** `404-555-0600`
- **After:** `404-555-0600 (Atlanta) or 704-555-0700 (Charlotte)`

### `greeting`
- **Added:** `Rapid Response Restoration, serving Atlanta and Charlotte`

### `integration_constraints`
- **Added:** `['do not reference Encircle to callers']`

### `office_address`
- **Before:** `3200 Peachtree Road NE, Atlanta GA 30305`
- **After:** `now also covers Charlotte, NC`

### `special_rules`
- **Added:** `['flag if caller says the property is vacant or abandoned', 'call Jerome directly at 404-555-0612 if caller says FEMA or federal disaster declaration']`

### `v1_to_v2_changes`
- **Added:** `{'added': ['ask for city and zip code early in the call to determine market', 'flag if caller says the property is vacant or abandoned', 'call Jerome directly at 404-555-0612 if caller says FEMA or federal disaster declaration'], 'updated': ['office_address', 'emergency_routing_rules.step_1.phone', 'emergency_routing_rules.step_1.contact_name', 'emergency_definition', 'integration_constraints', 'special_rules', 'greeting'], 'removed': []}`

## New Rules Added
- ask for city and zip code early in the call to determine market
- flag if caller says the property is vacant or abandoned
- call Jerome directly at 404-555-0612 if caller says FEMA or federal disaster declaration

## Agent System Prompt
- ✅ Updated to reflect all v2 changes

