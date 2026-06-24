---
comments: true
---

# Architectural Decisions

This section contains the Architecture Decision Records (ADRs) for the project.

ADRs document important architectural decisions and the reasoning behind them. They are historical records: once accepted, they should not be rewritten to match every later implementation detail. If the project changes direction, add a new ADR that supersedes or extends the earlier one.

## Current ADRs

* ADR-001: Adopt a Database-First Architecture Using PostgreSQL
* ADR-002: Separate Raw and Canonical Data Layers
* ADR-003: Store Raw Scraped Data Using JSONB
* ADR-004: Adopt an Entity-Centric Data Model Focused on Boats
* ADR-005: Pipeline Execution via CLI
* ADR-006: Centralised Configuration Management
* ADR-007: Structured Logging System

## Current Implementation Notes

The implementation has evolved beyond the earliest raw/canonical split in one important way: the database now also includes a `yacht_norm` schema for reviewable normalisation state, including club aliases and class/type aliases.

This does not invalidate the accepted raw/canonical separation. It adds an explicit middle layer:

```text
yacht_raw -> yacht_norm -> yacht_db
```

Future documentation or ADR work should capture this normalisation layer as its own architectural decision if it becomes a stable long-term contract.

## How To Use ADRs

When making changes:

* read the relevant ADRs before changing architecture
* treat accepted ADRs as constraints
* document new major decisions as new ADRs
* avoid silently changing database, pipeline or API architecture without recording the reason
