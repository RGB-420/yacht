---
comments: true
---

# Project Overview

## Purpose

The Regatta Data Platform is a structured data system for collecting, normalising and exploring sailing regatta information.

Regatta results are published across many websites and PDF formats with inconsistent structure, naming and data quality. The platform ingests those sources and turns them into a canonical dataset that can be queried, reviewed and used by applications.

The project is entity-centric. Regatta results are important because they reveal boats, classes, owners, clubs, schedules and relationships, but the platform is not primarily a race-results analytics system. Its core value is a clean, traceable registry of sailing entities discovered through regatta activity.

## Current Product Shape

The project now contains both backend and frontend application layers.

Current capabilities include:

* ingestion from many web result providers and selected PDF formats
* raw JSONB storage of scraped regatta results
* normalisation and mapping workflows for clubs, owners, classes and boat types
* canonical PostgreSQL tables for boats, owners, clubs, classes, types, regattas, editions, links, schedules and feedback
* FastAPI routes for exploration and feedback
* a React/Vite frontend called **Regatta Explorer**
* frontend pages for home/search, regattas, editions, boats, classes, clubs, calendar and admin feedback
* a user feedback flow, including admin-only review/update endpoints protected by `ADMIN_KEY`
* structured pipeline logging and centralised path configuration

## Current Phase

The project is in a private pilot/application-development phase.

The backend foundation is in place and the frontend is active. The main work is now about improving data completeness, operational stability, UI usefulness and the quality of the normalisation/review workflows.

Current priorities include:

* keeping ingestion and synchronisation pipelines reliable
* improving canonical data quality and mapping confidence
* expanding and hardening frontend exploration workflows
* improving API usability, pagination and filtering
* making feedback and review loops useful for data correction
* preparing the system for stable private deployment

## Core Technology

Current stack:

* Python for scraping, ETL and backend code
* PostgreSQL for raw, normalisation and canonical data
* FastAPI for the API layer
* SQLAlchemy for database access
* pandas for pipeline transformations
* Playwright, BeautifulSoup, requests and PDF/OCR libraries for ingestion
* React, TypeScript, Vite, React Router and TanStack Query for the frontend
* Tailwind CSS and lucide-react for UI styling and icons
* MkDocs, Material for MkDocs, Zensical and mkdocs-with-pdf for documentation

The operational flow is:

```text
External sources
  -> Scrapers
  -> Raw PostgreSQL storage
  -> Normalisation and sync pipelines
  -> Canonical PostgreSQL tables
  -> FastAPI
  -> React frontend
```

## Stakeholders

**David**  
Strategic oversight and product perspective. Provides governance guidance and reviews key architectural and project decisions.

**Raul**  
System architect and technical lead. Responsible for architecture design, data model definition, implementation decisions and AI-assisted development workflows.

**Elena**  
Supports data normalisation, validation and research of regatta data sources.

## Governance Model

The project separates governance and delivery concerns:

* GitHub tracks codebase and implementation history.
* Documentation records architecture, decisions and operating context.
* Lightweight coordination channels are used for operational updates.

Architecture Decision Records in `docs/decisions/` should be treated as accepted constraints. When implementation evolves beyond an ADR, a new ADR should be added rather than silently rewriting the historical decision.
