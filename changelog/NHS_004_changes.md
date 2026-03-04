# Changelog: Nordic HVAC Solutions (NHS_004)

**Version:** v1 → v2

**Date:** 2026-03-04T12:03:38.248539

**Summary:** Extended business hours, updated emergency routing rules, added new emergency trigger for data center failures, and updated greeting text.

## Changes (9 field changes)

### `business_hours.days`
- **Before:** `Monday-Friday`
- **After:** `Monday-Friday, Saturday`

### `business_hours.end`
- **Before:** `6:00 PM`
- **After:** `8:00 PM`

### `call_transfer_rules.if_no_answer`
- **Before:** `Collect caller information and call back within 1 business hour`
- **After:** `Callback within 30 minutes for medical facilities and server rooms, and 60 minutes for all others`

### `emergency_definition`
- **Added:** `['Any HVAC failure in a data center']`

### `emergency_routing_rules.fallback`
- **Before:** `Leave a voicemail at dispatch and send a notification`
- **After:** `None`

### `emergency_routing_rules.step_1.callback_guarantee`
- **Added:** `Callback within 30 minutes for medical facilities and server rooms, and 60 minutes for all others`

### `greeting`
- **Added:** `Nordic HVAC Solutions, commercial comfort specialists`

### `integration_constraints`
- **Added:** `['Do not quote any prices to callers']`

### `special_rules`
- **Added:** `["Immediate escalation to Ingrid at 612-555-0200 if caller identifies as calling from North Memorial Health or Children's Minnesota"]`

## New Rules Added
- Immediate escalation to Ingrid at 612-555-0200 if caller identifies as calling from North Memorial Health or Children's Minnesota

## Agent System Prompt
- ✅ Updated to reflect all v2 changes

