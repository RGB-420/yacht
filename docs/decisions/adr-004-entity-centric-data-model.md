# ADR-004: Adopt an Entity-Centric Data Model Focused on Boats

**Status:** Accepted
**Date:** 2026-03-06

## Context

The system collects information primarily from regatta result pages. These pages contain a mixture of data, including:

* boat names
* sail numbers
* owners
* club affiliations
* boat classes
* race results

However, the primary goal of the project has never been to build a database of race results. Instead, the objective is to construct a **structured dataset about boats and their associated entities**.

Regatta result pages are valuable because they often include detailed information about the participating boats, but they are treated primarily as **data sources** rather than the central subject of the system.

During early development it became clear that:

* The same boats appear repeatedly across multiple regattas.
* The most valuable information concerns the boats themselves and their relationships (owners, clubs, classes).
* Race positions provide little long-term value compared to the structural information about boats.

This led to the explicit decision to structure the system around **entities rather than events**.

## Decision

The platform adopts an **entity-centric data model** in which the primary focus is on boats and their relationships.

The canonical dataset therefore centres around entities such as:

* boats
* owners
* clubs
* boat classes
* locations

Regattas and regatta editions are retained in the data model, but primarily as **contextual metadata and discovery signals** for identifying boats and extracting information about them.

Race results themselves are not treated as the primary analytical dataset.

Boat identity is resolved during the normalisation process using a combination of:

* sail number (boat identifier)
* boat name similarity

Two records are considered to represent the same boat only when both conditions are satisfied:

* the sail number matches after normalisation
* the boat name is sufficiently similar

This approach allows the system to merge appearances of the same boat across different regattas while avoiding incorrect merges when identifiers are ambiguous.

## Consequences

Adopting an entity-centric model provides several advantages:

* The dataset focuses on durable entities rather than ephemeral race results.
* Boats appearing across multiple regattas can be unified into a single canonical record.
* Relationships between boats, clubs, and owners become easier to explore and analyse.
* The system produces a reusable knowledge base rather than a simple archive of race outcomes.

It also influences the structure of the canonical database:

* Many-to-many relationships are used for owners and clubs.
* Regattas act as contextual sources rather than the central dataset.
* Normalisation and identity resolution become critical components of the pipeline.

The main trade-off is that the system does not aim to preserve full analytical detail about race outcomes. Instead, it prioritises building a **clean and reliable registry of boats and related entities**.
