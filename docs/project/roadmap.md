---
comments: true
---

# Project Roadmap

This roadmap outlines the expected evolution of the Regatta Data Platform.

It is intended as a **strategic direction rather than a fixed commitment**, and phases may evolve as the project progresses.

The goal of the roadmap is to ensure the system evolves in a **structured and scalable way**, prioritising architectural stability before expanding functionality.

---

# Phase 0 – Architecture Stabilisation (Completed)

### Objective

Transform CSV-based workflows into a structured, database-driven system with operational pipelines and API access.

This phase focuses on establishing a **robust technical foundation** before expanding the platform.

### Environment

* Private GitHub repository
* Local development environment
* Docker used locally
* No external infrastructure cost

### Key Workstreams

**Database Foundation**

* Design PostgreSQL schema
* Define raw ingestion tables
* Define canonical relational tables
* Implement ingestion timestamping
* Establish traceability between raw and canonical data

**Pipeline Architecture**

* Refactor ingestion scripts to write directly to the database
* Create structured ingestion pipelines
* Introduce batch identifiers for traceability

**API Layer (Initial)**

* Establish FastAPI project structure
* Implement initial read-only endpoints
* Support basic filtering (year, confidence, source)

**Data Normalisation**

This workstream runs in parallel with the architecture build.

Activities include:

* defining normalisation rules
* mapping raw values to canonical entities
* assigning confidence levels
* documenting edge cases
* researching missing metadata

### Completion Criteria

* 2025 dataset stored in PostgreSQL
* Raw → canonical traceability operational
* API capable of querying structured data

### Achieved Outcomes

* Fully operational ETL pipelines
* Canonical PostgreSQL database in use
* FastAPI backend implemented
* Structured logging system in place
* CLI-based pipeline execution
---

# Phase 1 – Private Pilot (Current phase)

### Objective

Create a functional internal prototype usable by Raul and David.

### Environment

* Low-cost VPS (e.g. Hetzner)
* Docker deployment
* Private access only

### Key Goals

**Infrastructure**

* Deploy Docker stack to VPS
* Configure SSH access and firewall
* Implement automated database backups

**Dataset Completion**

* Complete ingestion of the 2025 dataset
* Perform data quality review
* Operationalise confidence scoring

**Semi-Automated Discovery**

* Maintain regatta calendar
* Introduce URL-based ingestion workflow
* Allow predefined ingestion workflows to be executed by junior contributors

**API & Product Layer**

* Improve endpoint design and performance
* Introduce pagination and filtering
* Enhance API documentation

**Frontend Development**

* Build initial React-based interface
* Enable data exploration (regattas, boats)
* Connect frontend to API endpoints

### Additional Focus Areas

* integration of frontend application
* improving API usability for exploration
* refining data quality and consistency

### Completion Criteria

* 2025 dataset trusted
* 2026 ingestion requires minimal manual effort
* Junior ingestion workflow stable
* System usable without developer intervention

---

# Phase 2 – Controlled Release

### Objective

Prepare the system for broader controlled access.

### Potential Infrastructure Evolution

* Evaluate migration to managed cloud infrastructure (e.g. AWS)
* Introduce monitoring and operational tooling

### Key Areas of Work

**Security & Access Control**

* User authentication
* Role-based access control
* Audit logging

**Operational Stability**

* Error monitoring
* Performance optimisation
* Backup and recovery validation

---

# Phase 3 – Scalable Production

This phase is not an immediate focus but represents the potential long-term evolution of the platform.

Possible areas of expansion include:

* multi-user access
* service-level reliability
* legal and compliance considerations
* expanded dataset coverage

---

# AI-Assisted Development (Cross-Phase Initiative)

AI tools are integrated throughout the project as a **development capability layer**.

Current and future exploration areas include:

* AI-assisted code generation
* architecture-aware refactoring
* automated test scaffolding
* anomaly detection in datasets
* rule suggestion for normalisation workflows
* conversational interaction with the dataset

AI is treated as:

* a productivity multiplier
* a structured development tool
* a capability to be explored incrementally

All AI-generated outputs remain **human-reviewed and architecturally supervised**.

---

# Ongoing Maintenance (From Pilot Phase)

Once the pilot phase is active, recurring operational tasks will include:

* monitoring ingestion failures
* reviewing low-confidence mappings
* adjusting schema when required
* dependency updates
* verifying backups
* reviewing system performance as the dataset grows
* monitoring API performance and usage
* maintaining frontend-backend integration
