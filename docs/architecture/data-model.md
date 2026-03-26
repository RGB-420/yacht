---
comments: true
---

# Data Model

## Overview

The data model is designed to build a structured registry of boats and their associated entities.

While regatta results are used as the primary source of information, the goal of the database is not to store detailed race results. Instead, regatta appearances act as a **discovery mechanism** for identifying boats and extracting structured information about them.

The canonical dataset therefore focuses on **boats and their relationships**, including owners, clubs, and classes.

The model follows a layered structure:

Raw Data → Normalisation → Canonical Entities

---

## Raw Data Layer

Raw scraped data is stored in the `yacht_raw` schema.

The table:

```
yacht_raw.raw_regatta_results
```

stores the extracted information for each regatta page as a JSON object.

Each record typically includes:

* source metadata
* regatta name
* year
* scraped timestamp
* structured raw data (`jsonb`)

This layer preserves the original extracted values and allows all transformations to be reproducible and traceable.

Raw data is never modified or deleted.

---

## Canonical Entity Model

The canonical schema (`yacht_db`) represents the structured dataset used by the system.

The model is centred around a set of core entities.

### Boats

The `boats` table represents the canonical identity of a boat.

Each boat is defined by:

* boat name
* boat identifier (typically a sail number)
* associated boat class

Boat identity is resolved during the normalisation process using:

* cleaned sail numbers
* fuzzy name matching
* manual review where required

This allows the system to recognise the same boat appearing across multiple regattas even when naming conventions differ.

---

### Owners

The `owners` table stores the canonical identities of boat owners.

A boat may have multiple owners.

The relationship is represented through the junction table:

```
boats_owner
```

which allows a many-to-many relationship between boats and owners.

---

### Clubs

The `clubs` table represents sailing clubs associated with boats.

Club records may include additional metadata such as:

* location
* short name
* estimated number of members

Boats may be affiliated with multiple clubs, represented through the junction table:

```
boat_clubs
```

---

### Boat Classes

The `boat_classes` table represents the general class of a boat, such as:

* Dragon
* Etchells
* J/70

Classes may include metadata such as:

* manufacturer
* rating rule
* crew size
* hull length

---

### Boat Types

The `boat_type` table provides a more specific classification within a class, representing particular boat models or variants.

This allows the system to distinguish between boats that belong to the same class but have different design variants.

---

### Regattas and Editions

Regattas are represented by two related tables:

```
regattas
regatta_editions
```

The `regattas` table represents the event itself, while `regatta_editions` represents a specific year of that event.

For example:

```
Cowes Week → Regatta
Cowes Week 2025 → Edition
```

This separation avoids duplication of event metadata across years.

---

### Boat Participation

The table:

```
boat_editions
```

records the participation of boats in specific regatta editions.

This information is used primarily as contextual metadata and as a discovery signal for identifying boats and their relationships.

The system does not aim to store full race result analytics.

---

### Locations

The `locations` table provides geographic metadata used by both clubs and regattas.

Typical attributes include:

* city
* region
* country

This allows geographic grouping and analysis of clubs and events.

---

## Entity Relationships

The model contains several many-to-many relationships:

Boat ↔ Owner
Boat ↔ Club
Boat ↔ Regatta Edition
Edition ↔ Class

These relationships are implemented using junction tables to preserve flexibility and avoid duplication.

---

## Normalisation Workflow

Raw values extracted from source pages are rarely consistent.

Normalisation currently follows a hybrid workflow:

1. Raw values are extracted from the JSON ingestion layer.
2. Lists of unique raw values are generated.
3. These values are reviewed and mapped to canonical entities.
4. Canonical entities are inserted into the database.

Mapping rules are currently stored in CSV lookup files but will eventually be migrated into database-managed mapping tables.

---

## Design Principles

The data model follows several key principles:

**Entity-centric design**
The system models boats and related entities rather than race results.

**Traceability**
All canonical entities can be traced back to raw source data.

**Flexibility**
Many-to-many relationships allow complex ownership and affiliation structures.

**Incremental normalisation**
Data quality improves over time through iterative normalisation.

**Separation of raw and canonical layers**
Raw scraped data is stored independently from the canonical relational model.
