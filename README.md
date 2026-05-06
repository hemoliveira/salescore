# SalesCore

> A full-stack sales management system built with Python, MySQL, and React.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=flat-square&logo=mysql&logoColor=white)
![React](https://img.shields.io/badge/React-18+-61DAFB?style=flat-square&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-5+-646CFF?style=flat-square&logo=vite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## Overview

SalesCore is a full-stack application for managing sales pipelines, tracking performance metrics, and generating business insights. It features a RESTful Python backend, a relational MySQL database with stored procedures and triggers, and a modern React frontend.

---

## Features

- 📊 Sales dashboard with real-time metrics
- 🗂️ Customer and deal management
- 🔄 Automated business rules via MySQL triggers and procedures
- 📈 Optimized queries and indexed views for reporting
- 🔐 Environment-based configuration for secure deployments
- ✅ Backend test suite with pytest

---

## Tech Stack

| Layer    | Technology                        |
|----------|-----------------------------------|
| Backend  | Python 3.11+, FastAPI, Pydantic   |
| Database | MySQL 8.0+                        |
| Frontend | React 18, Vite, ESLint            |
| Testing  | pytest                            |

---

## Project Structure

```
salescore/
├── backend/
│   ├── core/             # App configuration and database connection
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
│   ├── 01_create_tables.sql
│   ├── 02_functions.sql
│   ├── 03_views.sql
│   ├── 04_triggers.sql
│   ├── 05_procedures.sql
│   ├── 06_seed_data.sql
│   ├── 07_optimization.sql
│   └── 08_queries.sql
├── .gitignore
├── LICENSE
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- MySQL 8.0+

### 1. Clone the repository

```bash
git clone https://github.com/your-username/salescore.git
cd salescore
```

### 2. Set up the database

Connect to your MySQL instance and run the scripts in order:

```bash
mysql -u root -p < sql/01_create_tables.sql
mysql -u root -p < sql/02_functions.sql
mysql -u root -p < sql/03_views.sql
mysql -u root -p < sql/04_triggers.sql
mysql -u root -p < sql/05_procedures.sql
mysql -u root -p < sql/06_seed_data.sql
mysql -u root -p < sql/07_optimization.sql
```

### 3. Configure the backend

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` with your local settings:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=salescore
DB_USER=your_user
DB_PASSWORD=your_password
```

### 4. Run the backend

From the project root:

```bash
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
cd backend && uvicorn main:app --reload
```

API available at `http://localhost:8000`  
Interactive docs at `http://localhost:8000/docs`

### 5. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

App available at `http://localhost:5173`

---

## Running Tests

```bash
source .venv/bin/activate     # Windows: .venv\Scripts\activate
cd backend
pytest
```

---

## API Overview

| Method | Endpoint         | Description           |
|--------|------------------|-----------------------|
| GET    | `/health`        | Health check          |
| GET    | `/sales`         | List all sales        |
| POST   | `/sales`         | Create a sale         |
| GET    | `/sales/{id}`    | Get sale by ID        |
| PUT    | `/sales/{id}`    | Update a sale         |
| DELETE | `/sales/{id}`    | Delete a sale         |

> Full interactive documentation available via Swagger UI at `/docs`.

---

## Environment Variables

See `.env.example` for the full list of required variables. Never commit your `.env` file.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Author

Built by [Henrique Oliveira](https://github.com/hemoliveira) — open to freelance opportunities.  
Feel free to reach out via [LinkedIn](https://linkedin.com/in/henriquemo) or hemoliveira@gmail.com.
