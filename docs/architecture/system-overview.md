---
comments: true
---

# System Overview

## Architectural Philosophy

The system is designed as a **database-centric data platform**.

PostgreSQL acts as the **single source of truth** for all structured data.
All ingestion, normalisation and data access workflows are built around the database rather than file-based workflows.

The primary objective of the platform is to build a **structured registry of boats and related entities**, including owners, clubs, and classes.

Regatta results act primarily as a **data discovery source**, allowing the system to identify boats and extract associated information. The focus of the platform is therefore on **entity knowledge and relationships**, rather than on storing or analysing race results themselves.

This architecture ensures:

* traceability from raw data to canonical entities
* reproducibility of ingestion workflows
* clear separation between data storage and data consumption
* scalability as the dataset grows

The platform evolves from an initial script-based workflow toward a structured multi-layer architecture.

---

## High-Level Architecture

The system consists of several layered components:

Sources → Ingestion → Raw Storage → Normalisation → Canonical Data → API → Future UX

---

### 1. Data Sources

The system collects information from heterogeneous external sources, typically regatta result websites.

These sources often contain valuable information about boats and their associated entities but present several challenges:

* inconsistent formatting
* varying naming conventions
* incomplete metadata

Scrapers extract structured information about **boats and related entities** from these sources.
While the pages contain race results, the system primarily uses them as a **signal to identify boats and their attributes** such as class, club affiliation, and ownership.

---

### 2. Ingestion Layer

Scrapers retrieve regatta pages and extract structured information from them.

Each ingestion run collects:

* regatta metadata (as contextual information)
* boats appearing in the regatta
* associated attributes such as class, club, owner, or boat type

The extracted information for each regatta is stored together as a **JSON object**.

Ingestion pipelines are currently orchestrated through a Python execution entrypoint (`main.py`) which triggers the relevant scraping workflows.

---

### 3. Raw Data Storage

Raw scraped data is stored in PostgreSQL using **JSONB fields**.

Each record represents the raw extracted information for a single regatta and preserves the original values obtained from the source.

This layer acts as an **immutable record of the original source data**, enabling:

* reproducibility of transformations
* debugging of ingestion pipelines
* traceability between source data and canonical entities

Raw data is never modified or deleted.

---

### 4. Normalisation Pipeline

Raw data is processed through a Python normalisation pipeline.

The objective of this stage is to transform inconsistent raw values into a consistent canonical representation of entities.

Typical transformations include:

* mapping raw club names to canonical clubs
* mapping raw class names to canonical classes
* resolving boat identity across appearances
* validating or correcting inconsistent values

At the current stage, mapping rules are stored in **CSV-based lookup tables** used by the normalisation logic.

These mappings will eventually migrate into database-managed mapping tables.

Normalisation is designed to support a **human-in-the-loop workflow**, where edge cases and ambiguous values can be reviewed and corrected.

---

### 5. Canonical Database

After normalisation, structured entities are written to canonical relational tables.

Core entities include:

* boats
* owners
* clubs
* boat classes
* regattas and regatta editions (stored primarily as contextual metadata)

These tables form a **structured registry of boats and their relationships**.

The goal of the canonical dataset is to provide reliable information about boats and associated entities rather than detailed race results.

Each canonical entity can be traced back to the raw data that generated it.

---

### 6. API Layer

A FastAPI application provides structured access to the canonical dataset.

The API abstracts the database schema and exposes consistent endpoints for querying entities.

Typical responsibilities include:

* retrieving boats and their associated attributes
* exploring relationships between boats, clubs, owners, and classes
* filtering entities by attributes such as class or year
* exposing structured data for applications or analysis

The API layer decouples data storage from data consumption.

---

### 7. Future UX Layer

A web-based user interface will eventually sit on top of the API layer.

This interface is intended to support:

* exploring boats and their associated information
* understanding relationships between entities
* inspecting raw vs normalised values
* reviewing low-confidence mappings
* improving transparency and trust in the dataset

The UX will consume the API rather than interacting directly with the database.

---

## Execution Environment

The system is designed to run inside a containerised environment using Docker.

Typical components include:

* PostgreSQL database container
* ingestion pipeline container
* API container

Containerisation ensures reproducibility and simplifies deployment to future environments such as a VPS or managed cloud infrastructure.

---

## Architectural Principles

The platform follows several key design principles.

**Database-first architecture**
The database is the central system of record.

**Raw data preservation**
Original extracted data is stored unchanged for traceability.

**Human-in-the-loop normalisation**
Ambiguous data is resolved through structured human review.

**API-based access**
All external data access occurs through a controlled API layer.

**Layered architecture**
Each system layer has a clear and independent responsibility.

**Entity-focused dataset**
The platform focuses on building a reliable registry of boats and related entities, using regatta results as a discovery source rather than as the primary analytical dataset.
