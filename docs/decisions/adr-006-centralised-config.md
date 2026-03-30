---
comments: true
---

# ADR-006: Centralised Configuration Management

**Status:** Accepted  
**Date:** 2026-03-30

## Context

Early versions of the system relied on hardcoded paths and configuration values embedded directly within the codebase.

Examples included:

* file paths for data storage
* logging directories
* configuration values for execution

As the project evolved, this approach introduced several limitations:

* Reduced portability across environments
* Difficulty adapting the system for Docker or cloud deployment
* Increased risk of inconsistencies between modules
* Harder maintenance when configuration changes were required

A more flexible and environment-agnostic configuration system was required.

## Decision

The system adopts a **centralised configuration approach**, combining:

* environment variables (`.env`)
* a dedicated configuration module (`config.py`)

This configuration layer provides:

* centralised path management (data, logs)
* environment-based configuration
* separation between configuration and application logic

## Consequences

Benefits include:

* Improved portability across environments (local, Docker, future cloud)
* Easier configuration changes without modifying code
* Reduced duplication of configuration logic
* Better alignment with containerised deployment

Trade-offs include:

* Dependency on environment variables
* Requirement for consistent usage across the codebase

This decision establishes a flexible foundation for deployment and future system evolution.