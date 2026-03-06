# ADR-003: Store Raw Scraped Data Using JSONB

**Status:** Accepted
**Date:** 2026-03-06

## Context

The system collects information from multiple regatta result pages.
These sources are heterogeneous and often inconsistent in the data they provide.

For example, some regatta result pages may include:

* boat name
* sail number
* class
* club
* owner
* boat type

However, other sources may omit some of these attributes or present them in different combinations.

Examples of variation include:

* pages that include owner and class but no club
* pages that include club and class but no owner
* pages that include additional attributes not present in other sources

Because of this variability, the raw data extracted from each regatta cannot reliably fit into a fixed relational structure at the ingestion stage.

Initially, scraped data was exported to CSV files before being processed and inserted into the database.
As the architecture evolved toward a database-first model, it became preferable to store the raw data directly inside PostgreSQL.

## Decision

Raw scraped data is stored using a **JSONB column** in the raw ingestion table.

Example table:

```
yacht_raw.raw_regatta_results
```

Each row represents the raw data extracted from a single regatta page.

The extracted results are stored as a JSON object containing all records associated with that regatta.

Scraping pipelines typically follow this process:

```
scraper
    ↓
pandas dataframe
    ↓
df.to_dict(orient="records")
    ↓
JSONB storage in PostgreSQL
```

Using JSONB allows the system to store heterogeneous records without enforcing a rigid schema at the ingestion stage.

The responsibility for transforming these records into structured relational entities is delegated to the normalisation pipeline.

## Consequences

Using JSONB for raw ingestion provides several advantages:

* Flexibility when handling inconsistent source data
* Ability to store heterogeneous record structures
* Simplified ingestion pipelines
* Reduced schema maintenance at the scraping stage
* Easier debugging of raw extracted data

This approach allows scrapers to focus only on extracting available information, while the normalisation layer handles the complexity of mapping fields into the canonical data model.

The main trade-off is that JSONB data cannot be queried as efficiently as structured relational tables. However, this is acceptable because raw data is primarily used as input for the normalisation pipeline rather than as a query layer.

This design preserves the raw source information while keeping the canonical relational model clean and consistent.
