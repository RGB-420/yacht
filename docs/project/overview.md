---
comments: true
---

# Project Overview

## Purpose

The Regatta Data Platform is a structured data system designed to collect, normalise and expose regatta race data from heterogeneous sources.

Regatta results are often published across multiple websites with inconsistent formats and varying data quality.
The goal of this project is to ingest these sources and transform them into a **clean canonical dataset** that can act as a **source of truth for regatta results**.

This dataset is intended to support analysis, discovery, and future applications built on top of reliable structured data.

The platform also exposes this data through a structured API, enabling exploration and integration with external applications.

## Current Phase

The project is currently in an **early production-ready backend phase**, transitioning from prototype to application development.

The primary focus is on building a solid architectural foundation rather than releasing a finished product.

Current priorities include:

* maintaining and improving ingestion pipelines
* refining the canonical data model
* expanding API capabilities
* ensuring data quality and consistency
* preparing the system for frontend integration
* experimenting with AI-assisted development workflows

This stage prioritises **structural clarity and scalability** over feature completeness.

## Current Capabilities

The platform currently provides:

* automated data ingestion from multiple web and PDF sources
* ETL pipelines for data transformation and normalisation
* a canonical relational database (PostgreSQL)
* a fully implemented FastAPI backend
* structured logging for pipeline execution and monitoring
* an API for navigating regattas, boats and related entities

## Stakeholders

**David**
Strategic oversight and product perspective. Provides governance guidance and reviews key architectural and project decisions.

**Raul**
System architect and technical lead. Responsible for architecture design, data model definition, infrastructure decisions and AI-assisted development workflows.

**Elena**
Supports data normalisation, validation and research of regatta data sources.

## Core Technology

Current stack:

* Python (data processing and backend)
* PostgreSQL (canonical database)
* FastAPI (API layer)
* Playwright (web scraping)
* Docker (deployment and portability)

Development follows a layered model:

Data Sources → Ingestion → ETL Pipelines → Canonical Database → API → Frontend (in progress)

## Governance Model

The project uses a clear separation of responsibilities between systems:

* **GitHub** → codebase and technical implementation
* **Zensical** → governance, architecture documentation and decisions
* **Email / lightweight coordination** → operational updates and communication

This structure maintains a clear traceable history of architectural decisions while keeping development workflows lightweight.
