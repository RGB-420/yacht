---
comments: true
---

# AI Development Context

This document provides guidance for AI-assisted development tool working within this repository.

Its purpose is to help AI systems understand the structure of the project and the architectural constraints that must be respected when generating or modifying code.

AI tools are used in this project as a **development accelerator**, but all generated code remains subject to human review.

---

# Project Summary

The Regatta Data Platform is a structured data system designed to collect, normalise and expose information about sailing boats.

The system ingests regatta result pages and extracts structured information about boats and their associated entities.

The primary focus of the dataset is **boats and their relationships**, not race results.

Core entities include:

* boats
* owners
* clubs
* boat classes
* regattas and regatta editions

Regattas act primarily as **data sources for discovering boats and metadata**, rather than as the central dataset.

---

# Technology Stack

Current core technologies:

* Python
* PostgreSQL
* Docker
* FastAPI (planned API layer)

The development environment is containerised using Docker to ensure reproducibility across systems.

---

# Repository Structure

The repository is organised around a layered data architecture.

Typical components include:

* **scrapers**
  Responsible for extracting structured information from regatta result pages.

* **ingestion pipelines**
  Process scraped data and insert it into the raw database layer.

* **normalisation logic**
  Resolves raw values into canonical entities such as boats, clubs and owners.

* **database schema**
  Defines the canonical relational data model.

Future components will include:

* an API layer
* a user interface layer

---

# Architectural Principles

The system follows several architectural principles that must be respected by generated code.

### Database-first architecture

PostgreSQL acts as the **central system of record**.

All ingestion and processing workflows operate around the database rather than file-based storage.

### Raw vs canonical data separation

The database contains separate schemas for:

* raw ingestion data
* canonical relational entities

Raw data is stored unchanged and serves as the reproducible input for the normalisation pipeline.

### Flexible ingestion layer

Scraped raw data is stored as JSONB to support heterogeneous source structures.

Normalisation pipelines transform this data into structured relational entities.

### Entity-centric data model

The canonical dataset focuses on boats and their relationships.

Regattas act primarily as contextual sources of information.

---

# Architectural Decisions

Important architectural decisions are documented in the **ADR (Architecture Decision Record)** documents located in:

```
docs/decisions/
```

Examples include:

* database-first architecture
* separation of raw and canonical data
* JSONB storage for ingestion
* entity-centric data model

When generating code or suggesting architectural changes, these decisions must be **treated as constraints**.

If a proposed change conflicts with an ADR, the AI should highlight the conflict rather than silently ignoring the documented decision.

---

# Expected AI Contribution

AI tools may assist with:

* generating modules
* implementing pipelines
* writing API endpoints
* suggesting refactors
* improving documentation

AI-generated code should:

* follow the existing architectural structure
* respect the database schema and ADRs
* avoid introducing unnecessary abstractions
* prioritise clarity and maintainability

Large changes should be broken into clearly explained steps.

---

# Development Workflow

AI-generated code should be treated as **draft implementations** that require human validation.

Recommended workflow:

1. AI proposes implementation or module.
2. Human reviews architecture and logic.
3. Code is tested locally.
4. Adjustments are made before integration.

AI systems should prioritise **readable and explicit code** over overly complex abstractions.

---

# Future Stack Evolution

The backend will remain Python-based.

A frontend layer will likely be introduced in the future using a JavaScript framework (such as React or a similar tool), but this has not yet been finalised.

The API layer will expose structured access to the canonical dataset.

---

# Guiding Principle

AI is treated as a **capability multiplier**, not as an autonomous decision-maker.

Architectural integrity and data correctness always take priority over development speed.
