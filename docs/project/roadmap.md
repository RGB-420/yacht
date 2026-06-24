---
comments: true
---

# Project Roadmap

This roadmap describes the current direction of the Regatta Data Platform. It is strategic guidance rather than a fixed delivery contract.

## Phase 0 - Architecture Stabilisation (Completed)

### Objective

Move from exploratory CSV scripts to a structured database-first platform with ingestion, canonical data and API access.

### Achieved Outcomes

* PostgreSQL schemas for raw and canonical data
* JSONB raw ingestion storage
* canonical relational model for core entities
* FastAPI backend structure
* repository-based database access
* CLI-based pipeline execution
* structured logging
* centralised path configuration
* Architecture Decision Records documenting the foundational choices

## Phase 1 - Private Pilot And Application Build (Current)

### Objective

Turn the backend foundation into a useful private application for exploring and improving the dataset.

### Current State

The project now includes:

* active React/Vite frontend
* home search experience
* pages for regattas, editions, boats, classes, clubs and calendar
* feedback submission and admin review workflow
* schedule endpoint and calendar data path
* normalisation schema for club aliases and class/type aliases
* sync services for clubs, owners and class/type mappings

### Active Workstreams

**Data Quality**

* improve club, owner and class/type normalisation
* review pending aliases and unresolved mappings
* strengthen duplicate detection and relationship correctness
* keep master CSVs and database state aligned

**Ingestion**

* maintain existing web/PDF scrapers
* improve scrape queue operations
* reduce manual work for new regatta sources
* continue generating unscraped/pending source lists

**API**

* improve filtering and pagination coverage
* keep response schemas aligned with frontend needs
* document endpoint behavior as it stabilises
* harden error handling and admin flows

**Frontend**

* improve entity detail pages and relationship navigation
* make feedback flows clearer and more useful
* improve loading, empty and error states
* continue aligning UI with real API capabilities

**Operations**

* prepare a stable private deployment path
* define backup and restore procedures
* clarify environment variable setup
* improve documentation build/release workflow

### Completion Criteria

Phase 1 is complete when:

* the private frontend is useful without developer intervention
* ingestion and review workflows are repeatable
* the main 2025/2026 dataset is trusted enough for pilot use
* feedback can be reviewed and acted on reliably
* deployment and backup procedures are documented

## Phase 2 - Controlled Release

### Objective

Prepare the platform for broader controlled access beyond the initial private users.

### Key Areas

**Security And Access**

* authentication
* role-based access control
* safer admin tooling
* audit trail for corrections and review actions

**Operational Stability**

* monitored deployment
* automated backups
* error tracking
* performance checks for API and frontend

**Data Governance**

* clearer source provenance
* documented correction process
* confidence/review states exposed where useful

## Phase 3 - Scalable Production

This phase represents potential long-term growth.

Possible directions:

* public-facing product
* larger source coverage
* multi-user contribution workflows
* analytics and reporting layers
* richer entity history
* managed cloud infrastructure
* legal/compliance review for public data usage

## AI-Assisted Development

AI tools are part of the development workflow across phases.

Useful areas include:

* architecture-aware code changes
* documentation maintenance
* test scaffolding
* data anomaly detection
* normalisation rule suggestions
* review workflow assistance

AI-generated changes remain subject to human review, especially when they affect schema, data quality or architectural direction.
