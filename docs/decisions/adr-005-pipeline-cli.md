---
comments: true
---

# ADR-005: Pipeline Execution via CLI

**Status:** Accepted  
**Date:** 2026-03-30

## Context

Initially, data pipelines were executed through a single Python entrypoint (`main.py`), which triggered all ingestion and transformation workflows sequentially.

This approach was sufficient during early development, when the number of pipelines was limited and execution requirements were simple.

However, as the system evolved, several limitations became evident:

* Lack of flexibility when running individual pipelines
* Difficulty isolating and debugging failures
* Inefficient execution when only a subset of pipelines needed to run
* Reduced control over pipeline orchestration

The growing number of domain-specific pipelines (boats, classes, clubs, regattas, schedule, scraping) required a more modular and controllable execution model.

## Decision

The system adopts a **CLI-based pipeline execution model**, allowing each pipeline to be executed independently.

A command-line interface is introduced to:

* run individual pipelines
* run grouped pipelines when required
* provide a consistent execution interface

Each pipeline exposes a dedicated execution function, and the CLI acts as the orchestration layer.

## Consequences

This decision provides several benefits:

* Modular execution of pipelines
* Improved debugging and error isolation
* Greater flexibility in development workflows
* Better alignment with future scheduling and orchestration systems

Trade-offs include:

* Increased complexity compared to a single entrypoint
* Need to maintain a consistent interface across pipelines

Overall, the CLI-based approach improves scalability and maintainability of the pipeline system as the project grows.