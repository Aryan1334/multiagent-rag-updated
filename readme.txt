
# Multi-Agent Retrieval-Augmented Generation (RAG) API

This project implements a simple Retrieval-Augmented Generation (RAG) backend API using FastAPI and PostgreSQL. It exposes endpoints that accept natural language questions, generate corresponding SQL queries based on a fixed schema, execute them asynchronously against a PostgreSQL database, and return results in JSON format.

---

## Features

- Async connection pooling to PostgreSQL via `asyncpg`.
- Placeholder agent logic to map questions to SQL queries on `customers` and `orders` tables.
- API endpoints:
  - `POST /ask`: Accepts a JSON question, returns SQL results and a synthesized answer.
  - `GET /test`: Simple test query to fetch rows from the `customers` table.
- Designed as a backend API service (no built-in frontend UI).

---

## Requirements

- Python 3.8+
- PostgreSQL database with schema and sample data loaded (see **Database Setup**)
- Required Python packages (see `requirements.txt`)

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Aryan1334/multiagent-rag.git
cd multiagent-rag/multiagent-rag
