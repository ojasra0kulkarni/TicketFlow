# TicketFlow

A priority-aware ticket management system, built to demonstrate a clean full-stack app rather than enterprise-scale complexity. Practice/demo project — not production-hardened.

## Problem it addresses

Small teams (IT desks, internal ops, student helpdesks) often track support tickets in spreadsheets or chat threads: no standardized prioritization, no visibility into ticket state, no audit trail. TicketFlow gives them a lightweight, authenticated ticket tracker instead.

## Features

- **Authentication** — session-based login (Django `accounts` app)
- **Ticket lifecycle** — create tickets, filter/sort by priority (P1–P4), update status (Open → Closed), track raised/closed timestamps
- **Analytics dashboard** — total tickets, breakdown by status/priority/city, average resolution time (`ticketflowapp/analytics.py`)
- **CSV import/export** — bulk-load tickets via `import_csv.py`, export via `tickets_export.csv`
- **AI-assisted retrieval** *(planned)* — an `ai` Django app is scaffolded for semantic search over past tickets ("find similar historical tickets by description"); not implemented yet

## Architecture

Implemented as a Django monolith with server-rendered templates (an earlier design doc considered a separate Next.js frontend — that was not built; everything here is server-rendered Django):

```
TicketFlow/
  accounts/         auth
  core/              shared views/templates
  ticketflowapp/     Ticket model, CRUD views, analytics
  ai/                 scaffolding for semantic ticket retrieval (planned)
  ticketflow/        Django project settings/urls
```

Ticket fields: ID, priority (P1–P4), status (Open/Closed), subject, description, address/city, order ID, raised/closed timestamps. SQLite by default (`db.sqlite3`).

## Running locally

```bash
cd TicketFlow
python -m venv venv
venv\Scripts\activate        # Windows
pip install django            # no requirements.txt is committed yet — Django is the only hard dependency
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Target scale

Designed for clarity at ~1,000 tickets / single-organization usage — not distributed-systems scale.
