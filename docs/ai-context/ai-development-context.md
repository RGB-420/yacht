---
comments: true
---

# AI Development Context

This document helps AI-assisted development tools work safely and productively inside this repository.

AI may help write code, update documentation, inspect architecture, scaffold tests and diagnose issues. Human review remains required for implementation, data quality and architectural decisions.

## Project Summary

The Regatta Data Platform collects, normalises and exposes sailing regatta data.

The core dataset is entity-centric:

* boats
* owners
* clubs
* locations
* boat classes
* boat types
* regattas
* regatta editions
* schedules
* source links
* feedback

Regatta results are used primarily as discovery sources for durable entities and relationships.

## Current Stack

Backend and data:

* Python
* PostgreSQL
* SQLAlchemy
* FastAPI
* pandas
* Playwright
* BeautifulSoup
* requests
* PDF/OCR parsing libraries where needed

Frontend:

* React
* TypeScript
* Vite
* React Router
* TanStack Query
* Tailwind CSS
* lucide-react

Documentation:

* MkDocs
* Material for MkDocs
* mkdocs-with-pdf
* Zensical

## Repository Structure

Important areas:

* `scraping/` - web and PDF scrapers.
* `pipelines/` - domain pipelines and orchestration.
* `app/api/` - FastAPI app, routes and dependencies.
* `app/repositories/` - SQL/database access functions.
* `app/schemas/` - Pydantic response/request schemas.
* `app/services/` - normalisation, mapping, sync, aggregation, export and email services.
* `app/core/` - shared backend configuration and helpers.
* `db/` - schema, connection and database initialisation.
* `frontend/` - React/Vite frontend.
* `scripts/` - operational commands and reports.
* `docs/` - documentation and ADRs.

## Database Architecture

The project uses PostgreSQL as the system of record.

Schemas:

* `yacht_raw` stores raw scraper output.
* `yacht_norm` stores reviewable alias/mapping state.
* `yacht_db` stores canonical application data.

Generated code should respect this separation. Do not mix raw ingestion, normalisation review state and canonical API data without a clear reason.

## Pipeline Execution

Pipelines are run through:

```bash
python scripts/pipeline_cli.py run <pipeline>
```

Available pipeline names:

* `regattas`
* `classes`
* `clubs`
* `scrape`
* `boats`
* `full`

The full pipeline currently runs regattas, classes, clubs, scraping and boats in that order.

## API Architecture

FastAPI route modules should stay thin:

* validate request parameters
* call repository/service functions
* return schema-shaped data
* raise appropriate HTTP errors

Database access should generally live in `app/repositories/`.

Domain schemas should live in `app/schemas/`.

Admin feedback routes use `app/api/dependencies/admin.py` and the `ADMIN_KEY` environment variable.

## Frontend Architecture

The frontend lives in `frontend/` and consumes the API through `VITE_API_URL`.

Important conventions:

* routes are defined in `frontend/src/app/routes.tsx`
* navigation config lives in `frontend/src/shared/config/navigation.ts`
* API fetch helper lives in `frontend/src/shared/api/client.ts`
* feature modules live under `frontend/src/features/<domain>/`
* hooks encapsulate API reads for each feature

When adding frontend functionality, prefer the existing feature-based structure and shared components.

## Architectural Constraints

AI-generated changes should preserve these principles:

**Database-first**  
Use PostgreSQL-backed workflows for durable state.

**Raw/canonical separation**  
Raw scraped JSONB data and canonical application entities have different responsibilities.

**Normalisation remains reviewable**  
Ambiguous mappings should be surfaced for review instead of silently forcing questionable canonical values.

**Entity-centric model**  
The platform focuses on boats and relationships, not complete race-result analytics.

**Repository-backed API**  
Keep SQL out of route handlers unless there is a strong local precedent.

**Frontend through API**  
The React app should call FastAPI, not the database.

## ADRs

Architecture Decision Records live in:

```text
docs/decisions/
```

Treat accepted ADRs as constraints. If a change conflicts with an ADR, call out the conflict and propose a new ADR or explicit decision rather than silently changing direction.

## Expected AI Contribution

AI tools may assist with:

* code generation
* documentation updates
* bug diagnosis
* refactoring
* API/frontend alignment
* test scaffolding
* data-quality tooling

Generated code should be:

* explicit
* maintainable
* consistent with existing modules
* conservative around schema and data changes
* easy for a human maintainer to review

## Guiding Principle

Speed is useful only when it does not damage data correctness, traceability or architectural clarity.
