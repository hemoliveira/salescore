# SalesCore

> A full-stack sales management system built with Python, PostgreSQL, and React.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![React](https://img.shields.io/badge/React-19+-61DAFB?style=flat-square&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-8+-646CFF?style=flat-square&logo=vite&logoColor=white)
![Vercel](https://img.shields.io/badge/Deploy-Vercel-000000?style=flat-square&logo=vercel&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## Overview

SalesCore is a full-stack application for managing customers, products, and orders, with a dashboard for sales metrics. It features a RESTful Python backend, a PostgreSQL database (hosted on Neon) with functions, views, triggers, and stored procedures, and a modern React frontend. The project is deployed on Vercel, with the FastAPI backend running as a serverless function and the React app served statically.

---

## Features

- 📊 Sales dashboard with monthly metrics
- 🗂️ Customer, product, and order management (with order items)
- 🔄 Automated business rules via PostgreSQL triggers and procedures
- 📈 Optimized queries and indexed views for reporting
- 🔐 Environment-based configuration for secure deployments
- ✅ Backend test suite with pytest
- ▲ Ready to deploy on Vercel (serverless FastAPI + static frontend)

---

## Tech Stack

| Layer    | Technology                              |
|----------|------------------------------------------|
| Backend  | Python 3.11+, FastAPI, Pydantic, psycopg |
| Database | PostgreSQL (Neon)                        |
| Frontend | React 19, Vite, ESLint                   |
| Testing  | pytest                                   |
| Deploy   | Vercel                                   |

---

## Project Structure

```
salescore/
├── api/
│   └── index.py          # Vercel serverless entry point (wraps the FastAPI app)
├── backend/
│   ├── core/             # App configuration, DB pool, and logger
│   ├── models/           # Data models
│   ├── repositories/     # Database access layer
│   ├── routes/           # API route handlers
│   ├── schemas/          # Pydantic request/response schemas
│   ├── tests/            # pytest test suite
│   ├── main.py           # Application entry point
│   ├── .env.example      # Environment variable template
│   └── requirements.txt
├── frontend/
│   ├── src/              # React components and pages
│   ├── public/           # Static assets
│   └── index.html
├── sql/
│   ├── 00_create_database.sql
│   ├── 01_create_tables.sql
│   ├── 02_functions.sql
│   ├── 03_views.sql
│   ├── 04_triggers.sql
│   ├── 05_procedures.sql
│   ├── 06_seed_data.sql
│   ├── 07_optimization.sql
│   └── 08_queries.sql       # Example/reporting queries
├── package.json          # Root scripts to run frontend + backend together
├── vercel.json           # Vercel build/rewrite configuration
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- A PostgreSQL database (e.g. a free [Neon](https://neon.tech) instance)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/salescore.git
cd salescore
```

### 2. Set up the database

`00_create_database.sql` creates the `sales_core` database and the `salescore_app` role, so it must run against your server's default admin connection (`sales_core` doesn't exist yet):

```bash
psql "postgres://user:password@host:5432/postgres" -f sql/00_create_database.sql
```

> Using a managed provider like Neon? The database is provisioned for you when you create a project/branch — skip this script and grab the connection string it gives you.

Then run the remaining scripts against the `sales_core` database:

```bash
psql "$DATABASE_URL" -f sql/01_create_tables.sql
psql "$DATABASE_URL" -f sql/02_functions.sql
psql "$DATABASE_URL" -f sql/03_views.sql
psql "$DATABASE_URL" -f sql/04_triggers.sql
psql "$DATABASE_URL" -f sql/05_procedures.sql
psql "$DATABASE_URL" -f sql/06_seed_data.sql
psql "$DATABASE_URL" -f sql/07_optimization.sql
```

### 3. Configure the backend

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` with your connection string:

```env
DATABASE_URL=postgres://your_user:your_password@your_host.neon.tech/sales_core?sslmode=require
```

### 4. Install dependencies and run

From the project root, using the bundled npm scripts (starts backend + frontend together):

```bash
python -m venv .venv
.venv\Scripts\activate         # macOS/Linux: source .venv/bin/activate
npm run install:all
npm run dev                    # Windows
npm run dev:unix               # macOS/Linux
```

Or run each side manually in separate terminals:

```bash
# Backend
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
cd backend && uvicorn main:app --reload
```

```bash
# Frontend
cd frontend
npm install
npm run dev
```

API available at `http://localhost:8000`  
Interactive docs at `http://localhost:8000/docs`  
App available at `http://localhost:5173`

---

## Running Tests

```bash
source .venv/bin/activate      # Windows: .venv\Scripts\activate
cd backend
pytest
```

---

## API Overview

All routes are served under the `/api` prefix.

| Method | Endpoint                          | Description             |
|--------|------------------------------------|--------------------------|
| GET    | `/api/health`                      | Health check             |
| GET    | `/api/dashboard`                   | Monthly dashboard metrics|
| GET    | `/api/customers`                   | List customers           |
| POST   | `/api/customers`                   | Create a customer        |
| GET    | `/api/customers/{id}`              | Get customer by ID       |
| PUT    | `/api/customers/{id}`              | Update a customer        |
| DELETE | `/api/customers/{id}`              | Delete a customer        |
| GET    | `/api/products`                    | List products            |
| POST   | `/api/products`                    | Create a product         |
| GET    | `/api/products/{id}`               | Get product by ID        |
| PUT    | `/api/products/{id}`               | Update a product         |
| DELETE | `/api/products/{id}`               | Delete a product         |
| GET    | `/api/orders`                      | List orders              |
| POST   | `/api/orders`                      | Create an order          |
| GET    | `/api/orders/{id}`                 | Get order by ID          |
| PUT    | `/api/orders/{id}`                 | Update an order          |
| DELETE | `/api/orders/{id}`                 | Delete an order          |
| POST   | `/api/orders/{id}/items`           | Add an item to an order  |
| DELETE | `/api/orders/{id}/items/{item_id}` | Remove an item from an order |

> Full interactive documentation available via Swagger UI at `/docs`.

---

## Deployment

The project is set up to deploy on [Vercel](https://vercel.com):

- `vercel.json` builds the frontend (`frontend/dist`) as the static output and routes `/api/*` to `api/index.py`, a serverless wrapper around the FastAPI app.
- Set `DATABASE_URL` as an environment variable in your Vercel project settings (e.g. via a Neon Postgres integration from the Vercel Marketplace).

---

## Environment Variables

See `backend/.env.example` for the required variable. Never commit your `.env` file.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Author

Built by [Henrique Oliveira](https://github.com/hemoliveira) — open to freelance opportunities.  
Feel free to reach out via [LinkedIn](https://linkedin.com/in/henriquemo) or hemoliveira@gmail.com.
