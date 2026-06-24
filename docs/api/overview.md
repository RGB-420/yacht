---
comments: true
---

# Regatta Data API

The API is implemented with FastAPI in `app/api/main.py`.

Routes are grouped by domain under `app/api/routes/`, use Pydantic schemas from `app/schemas/` and read/write data through repository modules in `app/repositories/`.

The API is designed for entity exploration:

```text
Search
  -> Regattas
  -> Editions
  -> Boats
  -> Classes / Clubs / Owners / Types / Links / Schedule
```

## Common Patterns

List endpoints for boats and regattas support pagination:

```text
limit: 1..200, default 20
offset: >= 0, default 0
```

Paginated responses include:

* `data`
* `total`
* `limit`
* `offset`

Admin feedback endpoints require an `x-admin-key` header matching the backend `ADMIN_KEY` environment variable.

## Search

Global entity search.

```http
GET /search/?q={query}
```

The query must be at least two characters.

Returns grouped matches across searchable entities such as boats, regattas and classes.

## Regattas

```http
GET /regattas/?limit=20&offset=0
```

Lists regattas with pagination.

```http
GET /regattas/{regatta_id}
```

Returns one regatta by id.

```http
GET /regattas/{regatta_id}/editions
```

Returns all editions for a regatta.

## Editions

```http
GET /editions/{edition_id}
```

Returns one edition with its regatta context.

```http
GET /editions/{edition_id}/boats
```

Returns boats participating in an edition.

```http
GET /editions/{edition_id}/classes
```

Returns classes represented in an edition.

```http
GET /editions/{edition_id}/links
```

Returns external links associated with an edition.

## Boats

```http
GET /boats/?limit=20&offset=0
```

Lists boats with pagination.

```http
GET /boats/{boat_id}
```

Returns a boat detail record.

```http
GET /boats/{boat_id}/owners
```

Returns owners linked to a boat.

```http
GET /boats/{boat_id}/clubs
```

Returns clubs linked to a boat.

```http
GET /boats/{boat_id}/editions
```

Returns the boat's regatta edition participation history.

## Classes

```http
GET /classes/
```

Lists boat classes.

```http
GET /classes/{class_id}
```

Returns one class by id.

```http
GET /classes/{class_id}/boats
```

Returns boats associated with a class.

```http
GET /classes/{class_id}/types
```

Returns boat types under a class.

## Clubs

```http
GET /clubs/
```

Lists clubs.

```http
GET /clubs/{club_id}
```

Returns one club with detail fields.

```http
GET /clubs/{club_id}/boats
```

Returns boats associated with a club.

```http
GET /clubs/{club_id}/regattas
```

Returns regattas associated with a club.

## Schedule

```http
GET /schedule/
```

Returns scheduled regatta edition events with dates. This endpoint powers the frontend calendar.

## Feedback

```http
POST /feedback/
```

Creates a feedback item and schedules an email notification.

Feedback types currently include:

* `wrong_data`
* `missing_data`
* `duplicate`
* `wrong_relation`
* `broken_link`
* `other`
* `regatta_suggestion`

```http
GET /feedback
```

Admin-only. Lists feedback items.

```http
PATCH /feedback/{feedback_id}
```

Admin-only. Updates feedback status.

Allowed statuses:

* `pending`
* `reviewed`
* `fixed`
* `ignored`

## Project

```http
GET /project
```

Returns project-level metadata used by the application.

## Design Notes

The API is read-heavy and exploration-oriented. Most routes expose canonical entities and their relationships. Feedback is the main write workflow currently exposed to the frontend.
