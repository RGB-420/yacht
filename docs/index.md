---
comments: true
---

# Regatta Data Platform Documentation

This documentation describes the current architecture, backend, pipelines, frontend and operating model of the Regatta Data Platform.

The platform collects sailing regatta data from heterogeneous web and PDF sources, stores the extracted source data, normalises it into canonical entities and exposes the resulting dataset through a FastAPI API and a React frontend.

The project is now an integrated application, not only a backend prototype. The live codebase includes ingestion pipelines, normalisation workflows, a PostgreSQL data model, API routes, user feedback workflows and a frontend explorer.

## Current Status

The platform currently includes:

* web and PDF scraping modules for multiple regatta result providers
* PostgreSQL storage split across raw, normalisation and canonical schemas
* ETL pipelines for regattas, classes, clubs, scraping and boats
* CSV-backed master and review workflows used by the pipeline layer
* a FastAPI backend with entity, search, schedule, project and feedback routes
* a React/Vite frontend named **Regatta Explorer**
* global search, list/detail pages, calendar navigation and admin feedback review
* structured logging and centralised path configuration
* MkDocs/Zensical documentation generation

## Repository Areas

The main code areas are:

* `scraping/` - web and PDF scrapers.
* `pipelines/` - orchestration and domain-specific ETL pipelines.
* `app/` - API routes, schemas, repositories, services and application configuration.
* `frontend/` - React/Vite application that consumes the API.
* `db/` - database connection, initialisation and schema definition.
* `scripts/` - command-line utilities and operational helpers.
* `docs/` - project, architecture, API, ADR and AI-development documentation.

## Documentation Structure

### Project

High-level project purpose, current phase, product shape and roadmap.

### Architecture

System architecture, execution model, storage layers and design principles.

### Data Model

Current raw, normalisation and canonical database schemas and their entity relationships.

### API

The public FastAPI routes currently implemented by the backend.

### Architectural Decisions

Architecture Decision Records documenting accepted decisions and the constraints they introduce.

### AI Development Context

Guidance for AI-assisted development inside this repository.

## Download Documentation

You can download generated documentation artifacts when the documentation build has been run.

[Download PDF](pdf/document.pdf){ .md-button .md-button--primary }

[Download ZIP](download/regatta-docs.zip){ .md-button }

## Vision

The long-term goal is to become a reliable exploration and intelligence layer for sailing regattas, centred on boats and their relationships with classes, clubs, owners, regattas and editions.
