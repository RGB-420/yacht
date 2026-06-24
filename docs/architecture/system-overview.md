---
comments: true
---

# System Overview

## Architectural Philosophy

The system is a database-centric data platform.

PostgreSQL is the system of record for raw scraped data, normalisation state and canonical application data. Files are still used for master inputs, review workflows, reports and operational artifacts, but the database is the durable integration point for the API and application layer.

The platform remains entity-centric. Regatta sources are used to discover and enrich durable entities such as boats, owners, clubs, classes, boat types, editions and schedules.

## High-Level Architecture

```text
External web/PDF sources
  -> Scraping layer
  -> Raw storage (yacht_raw)
  -> Normalisation/review layer (yacht_norm + CSV review files)
  -> Canonical storage (yacht_db)
  -> Repository layer
  -> FastAPI routes
  -> React frontend
```

## 1. Data Sources

The scraping layer supports multiple result providers and custom sources, including web modules such as Halsail, Sailwave, Yacht Scoring, Clubspot, Manage2Sail, Cowes Week, J/70, Cape 31 and other regatta-specific sites.

PDF scraping is also represented through dedicated modules for Sailwave-style PDFs, Royal Solent PDFs and WLYC PDFs.

Sources vary widely in structure. The scraper layer extracts the information that is available and preserves it for downstream processing rather than forcing every source into one rigid ingestion schema.

## 2. Scraping And Ingestion

Scraping code lives under `scraping/`.

The scraping pipeline is triggered through `scripts/pipeline_cli.py` with the `scrape` pipeline. Its current flow is:

```text
sync scrape queue
  -> sync unscraped entries to master data
  -> run configured scrapers
  -> regenerate unscraped regatta list
```

Raw extracted data is stored in `yacht_raw.raw_regatta_results` as JSONB with source metadata, regatta name, year and scrape timestamp.

## 3. Normalisation And Review

Normalisation is implemented through services under `app/services/normalizers`, `app/services/mappings`, `app/services/sync` and `app/services/automapping`.

The codebase now has a dedicated `yacht_norm` schema for reviewable normalisation entities:

* `yacht_norm.clubs`
* `yacht_norm.club_aliases`
* `yacht_norm.club_alias_relations`
* `yacht_norm.class_types`
* `yacht_norm.class_type_aliases`
* `yacht_norm.class_type_alias_relations`

CSV files are still part of the workflow. They are used for master data, mapping inputs, generated review files and pending alias exports. These files support human-in-the-loop review while the database holds canonical and normalisation state.

## 4. Pipeline Layer

Pipelines live under `pipelines/` and can be run independently through:

```bash
python scripts/pipeline_cli.py run <pipeline>
```

Currently available pipeline names are:

* `regattas`
* `classes`
* `clubs`
* `scrape`
* `boats`
* `full`

The `full` pipeline currently runs:

```text
regattas -> classes -> clubs -> scrape -> boats
```

Domain pipelines combine file inputs, raw database reads, normalisation services and repository upserts. The boats pipeline is the main aggregation pipeline: it reads all raw results, normalises fields, synchronises clubs, owners and class/type aliases, generates master boat rows and writes boats plus relationship tables.

## 5. Canonical Database

Canonical data lives in `yacht_db`.

The core tables currently include:

* `regattas`
* `regatta_editions`
* `regatta_links`
* `regatta_schedule`
* `boats`
* `boat_type`
* `boat_type_relations`
* `owners`
* `clubs`
* `locations`
* `boat_classes`
* `edition_classes`
* `boats_owner`
* `boat_editions`
* `boat_clubs`
* `feedback`

This schema powers the API and frontend exploration experience.

## 6. API Layer

The API is a FastAPI application in `app/api/main.py`.

Routes are split by domain:

* `/regattas`
* `/editions`
* `/boats`
* `/classes`
* `/clubs`
* `/schedule`
* `/search`
* `/feedback`
* `/project`

The API uses route modules, Pydantic schemas and repository modules. Database sessions are provided through API dependencies, and admin-only feedback operations are protected through an `x-admin-key` header checked against `ADMIN_KEY`.

## 7. Frontend Layer

The frontend is an active React/Vite application under `frontend/`.

It consumes the API through `VITE_API_URL` and currently provides:

* a home/search page
* regatta list and detail pages
* edition detail pages
* boat list and detail pages
* class list and detail pages
* club list and detail pages
* calendar page backed by schedule data
* feedback submission components
* admin feedback review page
* light/dark theme support

Navigation is defined in `frontend/src/shared/config/navigation.ts`, and application routes are defined in `frontend/src/app/routes.tsx`.

## Execution Environment

The system is designed for local development and future private deployment.

Environment variables configure database access and API/frontend behavior. Important examples include:

* `DB_USER`
* `DB_PASSWORD`
* `DB_HOST`
* `DB_PORT`
* `DB_NAME`
* `PROJECT_DOCS_URL`
* `ADMIN_KEY`
* `VITE_API_URL`

Centralised path configuration lives in `app/core/config.py` and creates data/log directories such as `data/raw`, `data/master`, `data/mapping`, `data/review`, `data/queue`, `data/report`, `data/prenormalization`, `data/scorecard` and `logs`.

## Architectural Principles

**Database-first architecture**  
PostgreSQL is the integration point for raw, normalisation and canonical data.

**Raw data preservation**  
Scraped source data is preserved in JSONB before canonical transformation.

**Human-in-the-loop normalisation**  
Ambiguous clubs, owners, classes and types are resolved through reviewable mappings and sync workflows.

**Repository-backed API access**  
FastAPI routes use repository modules rather than embedding SQL directly in route handlers.

**Frontend consumes the API**  
The React application interacts with the backend through HTTP and does not connect directly to the database.

**Entity-focused dataset**  
The system prioritises durable sailing entities and relationships over complete race-result analytics.
