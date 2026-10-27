# ITSC 3155 – Assignment 5: Sandwich Maker CRUD API

Based on the instructor's [Assignment 5 starter](https://github.com/samfallahian/ITSC3155-Assignments/tree/main/Assignment5).

This FastAPI project implements create, read-all, read-one, update, and delete for all five tables: **sandwiches**, **resources**, **recipes**, **orders**, and **order_details**. The 20 required new endpoints extend the original Orders example.

## Project structure

- `api/models/models.py` — five SQLAlchemy table definitions and relationships
- `api/models/schemas.py` — Pydantic request and response schemas
- `api/controllers/` — modular CRUD functions for each table, including integrity-conflict handling
- `api/dependencies/` — MySQL configuration and SQLAlchemy database sessions
- `api/main.py` — 25 FastAPI endpoints, grouped by table in Swagger
- `api/tests/` — automated CRUD and error-handling tests

## Run with MySQL

Create the database in MySQL Workbench or the MySQL command line:

```sql
CREATE DATABASE sandwich_maker_api CHARACTER SET utf8mb4;
```

In PowerShell, from this repository's root folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:MYSQL_HOST = "localhost"
$env:MYSQL_PORT = "3306"
$env:MYSQL_DATABASE = "sandwich_maker_api"
$env:MYSQL_USER = "root"
$env:MYSQL_PASSWORD = "your_mysql_password"
uvicorn api.main:app --reload
```

Never commit your MySQL password. Application configuration uses environment variables. Open **http://127.0.0.1:8000/docs** for the Swagger API interface. On first start, SQLAlchemy creates the five tables in an empty database; it does not alter existing tables.

Create a sandwich, a resource, and an order before creating a recipe or order detail, since those tables refer to existing IDs.

### Sample POST request bodies

```json
// /sandwiches/  {"sandwich_name": "Turkey", "price": 7.50}
// /resources/   {"item": "Bread", "amount": 30}
// /orders/      {"customer_name": "John Doe", "description": "Lunch"}
// /recipes/     {"sandwich_id": 1, "resource_id": 1, "amount": 2}
// /order_details/ {"order_id": 1, "sandwich_id": 1, "amount": 1}
```

Use real IDs returned by the POST requests. For each table you can use GET on the collection and ID paths, PUT on an ID to update fields, and DELETE on an ID to remove it.

All five table groups return `201` when records are created, `200` when successfully read or updated, and `204` after deletion. Missing IDs return `404`, request validation errors return `422`, and database conflicts return `409`.

## Automated tests

```powershell
python -m pytest api/tests -q
```

The nine tests use an isolated SQLite database, with foreign-key enforcement enabled. They check CRUD operations for every table, order relationships, missing records, invalid values, duplicate names, and foreign-key violations. Passing these does **not** verify your local MySQL login; also run the app and test its API docs with MySQL.

## GitHub submission

Submit this repository's URL in Canvas: **https://github.com/victorathomas01-thinker/Assignment5**.

Commit messages use the Conventional Commits prefixes `feat:`, `test:`, and `docs:`. Before submission, **clone the repo locally and run an actual `git push`** after any changes, because the rubric explicitly requests that the code be pushed, not manually uploaded.

```powershell
git clone https://github.com/victorathomas01-thinker/Assignment5.git
cd Assignment5
# make any needed changes, then:
git add .
git commit -m "docs: record final MySQL verification"
git push origin main
```

Only commit if you have actual changes. Make your final commit before submitting on Canvas.
