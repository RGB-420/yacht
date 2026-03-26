---
comments: true
---

# Project Overview

## Purpose

The Regatta Data Platform is a structured data system designed to collect, normalise and expose regatta race data from heterogeneous sources.

Regatta results are often published across multiple websites with inconsistent formats and varying data quality.
The goal of this project is to ingest these sources and transform them into a **clean canonical dataset** that can act as a **source of truth for regatta results**.

This dataset is intended to support analysis, discovery, and future applications built on top of reliable structured data.

## Current Phase

The project is currently in a **prototype / private pilot phase**.

The primary focus is on building a solid architectural foundation rather than releasing a finished product.

Current priorities include:

* building a reliable ingestion pipeline
* defining the canonical data model
* validating the system architecture
* establishing structured governance
* experimenting with AI-assisted development workflows

This stage prioritises **structural clarity and scalability** over feature completeness.

## Stakeholders

**David**
Strategic oversight and product perspective. Provides governance guidance and reviews key architectural and project decisions.

**Raul**
System architect and technical lead. Responsible for architecture design, data model definition, infrastructure decisions and AI-assisted development workflows.

**Elena**
Supports data normalisation, validation and research of regatta data sources.

## Core Technology

Current stack:

* Python
* PostgreSQL
* FastAPI
* Docker

Development follows a layered model:

Data Sources → Ingestion → Canonical Database → API → Future UX Layer

## Governance Model

The project uses a clear separation of responsibilities between systems:

* **GitHub** → codebase and technical implementation
* **Zensical** → governance, architecture documentation and decisions
* **Email / lightweight coordination** → operational updates and communication

This structure maintains a clear traceable history of architectural decisions while keeping development workflows lightweight.
