<div align="center">

# TicketFlow

**A priority-aware support desk that tells you *where* your process is failing, not just how many tickets are open.**

[![Django](https://img.shields.io/badge/Django-5.x-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![pandas](https://img.shields.io/badge/pandas-analytics-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![SQLite](https://img.shields.io/badge/SQLite-default-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Status](https://img.shields.io/badge/status-demo%20project-orange)]()

</div>

Small teams — IT desks, internal ops, student helpdesks — usually track support tickets in a spreadsheet or a chat thread. No standard prioritisation, no visibility into what is stuck, no audit trail. TicketFlow is a lightweight authenticated tracker that fixes that, and then goes one step further: it runs a pandas analytics layer over the ticket table and renders seven charts that answer operational questions a raw list cannot.

> **Scope note:** this is a practice/demo project built for clarity at roughly 1,000 tickets and single-organisation usage. It is not production-hardened or distributed-systems scale, and the README says so rather than implying otherwise.

---

## The analytics layer

This is the part worth looking at. `ticketflowapp/analytics_utils.py` pulls the queryset into a DataFrame and generates every chart below with matplotlib on the `Agg` backend, writing them to `MEDIA_ROOT` for the dashboard to serve.

<table>
<tr>
<td width="50%"><img src="TicketFlow/media/priority_heat.png" alt="Open ticket percentage by priority"></td>
<td width="50%"><img src="TicketFlow/media/avg_resolution.png" alt="Average resolution time by priority"></td>
</tr>
<tr>
<td align="center"><b>Open % by priority</b><br><em>Backlog pressure, normalised. P1 at 40% open is a different emergency from P4 at 40%.</em></td>
<td align="center"><b>Mean resolution hours by priority</b><br><em>Whether P1 actually gets treated as critical, or the labels are decorative.</em></td>
</tr>
<tr>
<td><img src="TicketFlow/media/top5_cities.png" alt="Top 5 problem cities"></td>
<td><img src="TicketFlow/media/city_leaderboard.png" alt="City performance leaderboard"></td>
</tr>
<tr>
<td align="center"><b>Top 5 problem cities</b><br><em>Raw volume by location.</em></td>
<td align="center"><b>City performance leaderboard</b><br><em>Volume rewards big cities. This scores <code>closure_rate ÷ avg_resolution_hours</code> instead, so a small fast city beats a large slow one.</em></td>
</tr>
<tr>
<td><img src="TicketFlow/media/top_subjects.png" alt="Top recurring problems"></td>
<td><img src="TicketFlow/media/cluster_share.png" alt="Cluster-wise ticket share"></td>
</tr>
<tr>
<td align="center"><b>Top recurring problems</b><br><em>The five most repeated subject lines — candidates for a fix rather than a ticket.</em></td>
<td align="center"><b>Issue category share</b><br><em>Keyword classifier bucketing every ticket into Delivery / Inventory / Product / Shipping / Other.</em></td>
</tr>
</table>

### The city leaderboard is the interesting one

Ranking cities by ticket volume just ranks them by population. The leaderboard uses a composite instead:

```python
performance_score = (closed_tickets / total_tickets) * (1 / avg_resolution_hours)
```

Closure rate divided by mean resolution time — a city only scores well if it closes most of what it receives *and* closes it quickly. In the sample data that puts **Bhopal** and **Indore** on top while Bangalore and Ahmedabad sit at the bottom, an ordering that raw volume completely inverts.

The analytics module also derives `fastest_city` / `slowest_city` and returns them alongside the chart URLs for the dashboard to display.

### Issue clustering

"Clustering" here is honest about what it is — a keyword rule, not a model:

| Bucket | Matches on |
|---|---|
| Delivery Issues | `delay`, `late`, `delivery` |
| Inventory Issues | `stock`, `inventory`, `out of stock` |
| Product Issues | `damaged`, `wrong item`, `defective` |
| Shipping Issues | `shipping`, `courier`, `tracking` |
| Other | everything else |

Cheap, transparent, and adequate for five categories. It is also the obvious place where the scaffolded `ai` app would eventually replace rules with embeddings.

---

## Features

- **Authentication** — session-based login via the `accounts` app
- **Ticket lifecycle** — create, filter and sort by priority (P1–P4), move Open → Closed, with `raised_at` / `closed_at` timestamps
- **Analytics dashboard** — totals, breakdowns by status / priority / city, mean resolution time, plus the seven charts above
- **CSV import/export** — bulk load via `import_csv.py`; `tickets_export.csv` ships with **1,000 sample tickets** so the dashboard has something to render immediately
- **AI-assisted retrieval** — *not implemented.* The `ai` app is scaffolded and `ai/retrieval.py` is currently an empty file. The intent is semantic search over historical tickets ("find similar past tickets by description").

---

## Data model

`ticketflowapp/models.py` — one table, deliberately:

| Field | Type | Notes |
|---|---|---|
| `ticket_id` | CharField, unique | Business ID, e.g. `3P1000` |
| `priority` | Choice | `P1` Critical · `P2` High · `P3` Medium · `P4` Low |
| `status` | Choice | `OPEN` · `CLOSED` |
| `subject` | CharField(255) | Drives the recurring-problem and clustering charts |
| `description` | TextField | |
| `address` | CharField(255) | City — drives all geographic analytics |
| `order_id` | CharField(50) | Links a ticket to an order |
| `raised_at` | DateTime | |
| `closed_at` | DateTime, nullable | Null means still open; resolution time is `closed_at - raised_at` |
| `created_at` | DateTime, auto | |

---

## Architecture

A Django monolith with server-rendered templates. An earlier design doc considered a separate Next.js frontend; that was not built, and everything here is server-rendered.

```
TicketFlow/
  accounts/          authentication
  core/              shared views, templates, context processors, template tags
  ticketflowapp/     Ticket model, CRUD views
    analytics.py       queryset aggregates (totals, averages, breakdowns)
    analytics_utils.py pandas + matplotlib chart generation
  main/              additional views
  ai/                scaffolding for semantic retrieval (empty)
  ticketflow/        project settings and root urls
  media/             generated chart PNGs
  import_csv.py      bulk loader
  tickets_export.csv 1,000 sample tickets
```

Two analytics modules by design: `analytics.py` does cheap ORM-level aggregation for the summary cards, `analytics_utils.py` does the expensive DataFrame work for the charts.

---

## Running locally

```bash
cd TicketFlow
python -m venv venv
venv\Scripts\activate              # Windows
# source venv/bin/activate         # macOS / Linux

pip install django pandas numpy matplotlib seaborn

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

No `requirements.txt` is committed. Django is the only hard dependency for the app itself; `pandas`, `numpy`, `matplotlib` and `seaborn` are required for the analytics dashboard.

Load the sample data:

```bash
python import_csv.py
```

---

## Repository health

> [!WARNING]
> **This repository has its entire virtualenv committed** — 13,538 files under `env/`, roughly 240 MB, cloned by anyone who touches it.
>
> The cause is a real bug rather than an oversight: `.gitignore` already lists `env/`, `__pycache__/`, `*.pyc` and `db.sqlite3`, but the file was saved as **UTF-16LE with a BOM**. Git reads `.gitignore` as UTF-8 bytes, so the first pattern parses as `\xff\xfee\x00n\x00v\x00/` — nonsense that matches nothing. Every rule in the file was silently inert.
>
> The encoding is fixed in this commit, which stops the problem from recurring. It does **not** untrack what is already tracked: `.gitignore` has no effect on files git is already following. Clearing them needs an explicit
> ```bash
> git rm -r --cached env db.sqlite3
> ```
> and the history would still carry the blobs until rewritten.

`db.sqlite3` is committed for the same reason, which means the database ships with the code.

---

## Target scale

Built for clarity at ~1,000 tickets and one organisation. The analytics layer loads the full queryset into a DataFrame on every dashboard request, which is fine at this size and the first thing that would need caching at a larger one.
