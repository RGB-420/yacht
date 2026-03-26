---
comments: true
---

# ADR-002: Separate Raw and Canonical Data Layers

**Status:** Accepted
**Date:** 2026-03-06

## Context

During the early stages of the project, scraped data was stored in CSV files before being processed and inserted into the database.

While this approach worked for initial experimentation, it created several problems as the project evolved into a structured data platform:

* Raw data existed outside the main system of record
* It was harder to reproduce transformations
* The ingestion workflow relied on multiple intermediate files
* Debugging and auditing transformations became more difficult

To simplify the architecture and maintain a consistent system of record, raw data ingestion was moved directly into the PostgreSQL database.

However, raw data and canonical data serve fundamentally different purposes and therefore should not share the same schema.

Raw data represents **unprocessed source information**, while canonical tables represent **cleaned and structured entities** used by the application.

## Decision

The system separates raw and canonical data into different database schemas.

Two primary schemas are used:

```
yacht_raw
yacht_db
```

The `yacht_raw` schema stores raw ingestion data exactly as extracted by scrapers.

Example table:

```
yacht_raw.raw_regatta_results
```

Each record stores the raw extracted data for a regatta page as a JSONB object along with metadata such as source URL and scrape timestamp.

The `yacht_db` schema stores the canonical relational model used by the platform, including entities such as:

* boats
* owners
* clubs
* boat classes
* regattas and regatta editions

Raw data is treated as **immutable source input**, while canonical tables are generated through the normalisation pipeline.

The normalisation process always runs against the complete raw dataset, ensuring that improvements to the normalisation logic automatically propagate to all records.

## Consequences

Separating raw and canonical layers provides several benefits:

* Clear distinction between ingestion data and trusted canonical entities
* Full traceability from canonical entities back to their raw source data
* Ability to reprocess the entire dataset when normalisation logic improves
* Simplified ingestion pipeline (scrapers write directly to the database)
* Reduced risk of accidental modification of source data

It also establishes a clean layered architecture:

```
Scrapers
    ↓
Raw ingestion (yacht_raw)
    ↓
Normalisation pipeline
    ↓
Canonical entities (yacht_db)
```

This design supports incremental improvements to data quality while preserving the original source data used to build the dataset.

The main trade-off is that the system stores both raw and processed data, which increases storage usage. However, the benefits in traceability and reproducibility outweigh this cost.
