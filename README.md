# TicketFlow
Simple ticketing tool that has a frontend and a backend.(This tool is just for practice and demonstration purpose.)
Project Title

Priority-Aware Ticket Management System with Web Dashboard and Knowledge Retrieval

Problem Statement

Organizations that handle operational or technical workflows (IT support desks, internal operations teams, student helpdesks, etc.) receive large numbers of service requests (“tickets”).
In small or semi-manual environments these tickets are often tracked using spreadsheets, chat groups, or email threads. This creates several systemic issues:

• No standardized prioritization
• Poor visibility of ticket state
• No audit trail of actions taken
• Difficult status updates
• Hard to extract operational insights
• Repeated human effort answering similar issues

Therefore, there is a need for a lightweight web-based ticket tracking system that:

Standardizes ticket recording

Tracks lifecycle (open → closed)

Enables controlled updates

Provides simple analytics

Allows quick retrieval of historical knowledge

The system must remain intentionally simple to demonstrate correct understanding of frontend–backend interaction rather than enterprise-level complexity.

Objective

Design and implement a full-stack web application that allows authenticated users to:

• Create tickets
• View and filter tickets by priority
• Update ticket status and remarks
• Track history of ticket handling
• View simple analytics dashboard
• Retrieve similar past tickets using semantic search (optional RAG extension)

Target dataset scale: ≈ 1000 tickets

Functional Requirements
Authentication

Users must log in before accessing the system.

Purpose:
Not security complexity — but demonstration of session/state handling across frontend and backend.

Ticket Entity

Each ticket contains:

Ticket ID
Priority: P1 / P2 / P3
Description
Status: Open / Closed
Remarks (editable)
Timestamp

Core Features
Ticket Listing Page

Displays all tickets.

Capabilities:
• Filter by priority
• Sort by status
• Visual differentiation of P1 / P2 / P3
• Click → open detailed ticket view

This demonstrates API data fetching + UI rendering.

Ticket Detail Page

Shows full information of selected ticket.

Actions allowed:
• Change status (Open → Closed)
• Add remarks

This demonstrates:
State mutation → backend update → frontend refresh

Ticket Creation

Users can add a new ticket from UI.

Purpose:
Demonstrates POST request + persistence.

Analytics Page

Simple aggregated statistics:

• Number of open tickets
• Closed tickets
• Tickets by priority
• Possibly: average closure distribution

No advanced BI — only aggregation queries.

This demonstrates backend data processing + frontend visualization.

Optional RAG Extension (If time permits)

Add a search box:

User types a problem description → system retrieves similar past tickets.

Purpose:
Not chatbot — only retrieval assistance.

This demonstrates understanding of:
Data indexing vs data storage

Non-Functional Requirements

The system intentionally optimizes for clarity rather than scale:

• Supports ~1000 records
• Single organization usage
• No real-time synchronization needed
• No distributed systems required

Goal: demonstrate fundamentals, not infrastructure engineering.

System Architecture (Conceptual)

Client (Next.js UI)
↓ HTTP/JSON
Server (Django REST backend)
↓
Database (ticket storage)

Optional:
Vector Index (for retrieval search)

This project specifically demonstrates separation of concerns:
Presentation ↔ Business Logic ↔ Data

Rendering Strategy (Important Design Choice)

You should use a hybrid model:

Use Server-Side Rendering (SSR)

For:
• Ticket list page
• Analytics dashboard

Reason:
Data changes frequently → must always be fresh
Tickets are operational data, not static content

Use Client-Side Rendering (CSR)

For:
• Ticket detail interaction
• Status updates
• Adding remarks

Reason:
Interactive updates without page reload
Better UX and demonstrates API integration

Do NOT use Static Site Generation (SSG)

Because:
Tickets are dynamic operational data
Pre-rendering would be conceptually incorrect

Why This Project Is Academically Strong

This project demonstrates real understanding of:

Authentication state
REST communication
CRUD lifecycle
Frontend state management
Server business logic
Data modeling
Data aggregation
Optional semantic retrieval

Not just “making pages” — but understanding system behavior.
