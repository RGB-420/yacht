---
comments: true
---

# Regatta Data Platform Documentation

This documentation describes the architecture, backend system and API of the Regatta Data Platform.

The platform is a fully functional data system for sailing regattas, including data ingestion, processing pipelines and a public API layer.

The goal of this documentation is to provide a clear and structured overview of the system for developers, collaborators and AI-assisted development tools.

## Current Status

The platform currently includes:

- Data ingestion pipelines (web scraping and PDF parsing)
- ETL processing and canonical data model
- Fully implemented FastAPI backend
- Structured logging and execution tracking
- API endpoints for exploring regattas, boats and related entities

A frontend application is currently under development.

## Download Documentation

You can download the complete documentation or access the Markdown source.

[📄 Download PDF](pdf/document.pdf){ .md-button .md-button--primary }

[📦 Download ZIP](download/regatta-docs.zip){ .md-button }

## Documentation Structure

### Project

High-level information about the project and its evolution.

* Project overview
* Project roadmap

### Architecture

Technical documentation describing how the system is structured.

* System architecture
* Data model

### API

Documentation of the FastAPI backend and available endpoints.

* API overview
* Endpoint structure
* Data navigation model

### Architectural Decisions

Architecture Decision Records (ADRs) documenting key design choices.

### AI Development Context

Guidelines for AI-assisted development and how AI tools interact with the project.

## Purpose of this Documentation

This documentation exists to:

* document the architecture and backend system of the platform
* provide governance and technical clarity
* support AI-assisted development workflows
* ensure long-term maintainability of the system
* provide a clear interface for interacting with the data via the API

## Vision

The long-term goal of the platform is to become a comprehensive data exploration tool for sailing regattas, combining structured data, analytics and user-facing applications.