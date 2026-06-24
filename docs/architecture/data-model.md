---
comments: true
---

# Data Model

## Overview

The data model is organised into three PostgreSQL schemas:

```text
yacht_raw  -> raw scraped source data
yacht_norm -> reviewable normalisation and alias state
yacht_db   -> canonical application data
```

The canonical model is centred on boats and their relationships with owners, clubs, classes, types, regattas, editions and schedules.

## Raw Data Layer

Raw scraped data is stored in:

```text
yacht_raw.raw_regatta_results
```

Each row represents one scraped regatta source and includes:

* `source_type`
* `source_page`
* `regatta_name`
* `year`
* `scraped_at`
* `raw_data` as JSONB

This layer preserves heterogeneous source structures and gives the pipeline layer a reproducible input.

## Normalisation Layer

The `yacht_norm` schema stores reviewable alias and mapping state used by normalisation workflows.

Current normalisation tables include:

* `clubs` - canonical normalisation-level club names and metadata.
* `club_aliases` - raw club names, normalised values, status, confidence and review metadata.
* `club_alias_relations` - relationships between aliases and normalised clubs.
* `class_types` - canonical class/type pairs.
* `class_type_aliases` - raw class/type pairs, normalised values, status, confidence and review metadata.
* `class_type_alias_relations` - relationships between aliases and canonical class/type records.

This schema supports human review, automated mapping suggestions and repeatable sync into canonical entities.

## Canonical Schema

The `yacht_db` schema is the application-facing model used by the API and frontend.

### Regattas And Editions

`regattas` stores the stable event identity.

Key fields:

* `id_regatta`
* `name`
* `type`
* `id_club`
* `id_location`
* `created_at`

`regatta_editions` stores the year-specific instance of a regatta.

Key fields:

* `id_edition`
* `id_regatta`
* `year`
* `status`
* `created_at`

This allows a single event such as Cowes Week to have multiple yearly editions.

### Regatta Links And Schedule

`regatta_links` stores source or reference URLs for editions.

`regatta_schedule` stores start and end dates per edition and powers the frontend calendar/API schedule view.

### Boats

`boats` stores canonical boat identities.

Key fields:

* `id_boat`
* `name`
* `boat_identifier`
* `id_type`
* `created_at`

The unique key is currently `(name, boat_identifier)`.

### Owners

`owners` stores canonical owner names.

The many-to-many boat-owner relationship is stored in:

```text
yacht_db.boats_owner
```

### Clubs And Locations

`clubs` stores canonical club records.

Key fields:

* `name`
* `short_name`
* `estimated_numbers`
* `id_location`

`locations` stores city, region and country values. Clubs and regattas can reference locations.

The many-to-many boat-club relationship is stored in:

```text
yacht_db.boat_clubs
```

### Classes And Boat Types

`boat_classes` stores higher-level class data such as manufacturer, category, rating rule, start year, crew range and length.

`boat_type` stores more specific type/model records and can reference a class.

The model currently supports both:

* `boats.id_type` as a direct type reference
* `boat_type_relations` as a many-to-many boat/type relationship

`edition_classes` records which classes appear in each regatta edition.

### Boat Participation

`boat_editions` records which boats appear in which regatta editions.

This is the core bridge between discovered regatta participation and canonical boat records.

### Feedback

`feedback` stores user-submitted corrections, missing-data reports, duplicate reports, broken-link reports and regatta suggestions.

Feedback status values are:

* `pending`
* `reviewed`
* `fixed`
* `ignored`

Feedback is used by the frontend and admin review workflow.

## Main Relationships

The main relationship tables are:

* `boats_owner`: boats to owners
* `boat_clubs`: boats to clubs
* `boat_editions`: boats to regatta editions
* `edition_classes`: editions to classes
* `boat_type_relations`: boats to boat types

Conceptually:

```text
Regatta -> Edition -> Boat
Edition -> Class
Boat -> Owner
Boat -> Club
Boat -> Type -> Class
Regatta/Club -> Location
Edition -> Link
Edition -> Schedule
```

## Normalisation Workflow

The current workflow combines raw database reads, CSV master/review files and database-backed normalisation tables:

1. Scrapers insert raw JSONB results.
2. Regatta, class and club master files seed canonical reference data.
3. Sync pipelines update scrape queues, master CSVs and normalisation tables.
4. Raw boat rows are normalised into consistent column names and values.
5. Club, owner and class/type sync workflows resolve or flag aliases.
6. The boats pipeline writes canonical boats, owners, types, clubs and relationship rows.
7. Pending aliases and unresolved cases are exported for review.

## Design Priorities

**Traceability**  
Raw data is retained separately from canonical entities.

**Reviewability**  
Ambiguous names and class/type values can be reviewed and mapped over time.

**Application readiness**  
Canonical tables are shaped for API and frontend navigation.

**Entity focus**  
Race participation is used to discover durable entities and relationships.
