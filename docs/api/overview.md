# Regatta Data API

This document describes the available endpoints of the Regatta Data API.

The API is designed around a hierarchical navigation model:

**Regattas → Editions → Boats → Related entities (Classes, Clubs, Owners)**

---

## Search

Global search across entities.

GET /search?q={query}

Returns matching:
- Boats
- Regattas
- Classes

---

## Regattas

Access regatta information and related data.

GET /regattas  
→ List all regattas  

GET /regattas/{id}  
→ Get detailed information about a specific regatta  

GET /regattas/{id}/editions  
→ List all editions of the regatta  

GET /regattas/{id}/links  
→ External sources (official pages, results)

---

## Editions

Access information about a specific regatta edition.

GET /editions/{id}  
→ Edition metadata (year, status, regatta)

GET /editions/{id}/boats  
→ Boats participating in the edition  

GET /editions/{id}/classes  
→ Classes present in the edition  

---

## Boats

Access boat data and relationships.

GET /boats  
→ List boats (supports future pagination)

GET /boats/{id}  
→ Detailed boat information:
- class
- type
- owners
- clubs

GET /boats/{id}/owners  
→ Boat owners  

GET /boats/{id}/clubs  
→ Boat clubs  

GET /boats/{id}/editions  
→ Participation history  

---

## Classes

Access boat class information.

GET /classes  
→ List all classes  

GET /classes/{id}  
→ Class details  

GET /classes/{id}/boats  
→ Boats belonging to the class  

GET /classes/{id}/types  
→ Types within the class  

---

## Clubs

Access club information.

GET /clubs  
→ List all clubs  

GET /clubs/{id}  
→ Club details  

GET /clubs/{id}/boats  
→ Boats associated with the club  

GET /clubs/{id}/regattas  
→ Regattas organized by the club  

---

## Design Notes

- The API follows an **entity-centric model focused on boats**
- Relationships are exposed through dedicated endpoints
- The API is designed for **exploration and analysis**, not just retrieval