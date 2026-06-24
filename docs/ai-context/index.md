---
comments: true
---

# AI Development Context

This section documents how AI-assisted development should work inside the Regatta Data Platform.

The goal is to give AI tools enough architectural context to make useful changes without drifting away from the project's database-first, entity-centric design.

AI can help with:

* code generation and refactoring
* architecture review
* documentation maintenance
* test scaffolding
* API/frontend alignment
* pipeline and data-quality investigation

AI is a development accelerator, not an autonomous decision-maker. Generated output should be reviewed by a human maintainer, especially when it touches schema, data quality, ingestion behavior or architectural boundaries.

## Contents

* **AI Development Context** - repository structure, architectural constraints and implementation guidance for AI-assisted development.
