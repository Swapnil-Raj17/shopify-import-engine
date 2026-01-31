# Shopify Import Engine (Matrixify-Lite)

A standalone, asynchronous product import and synchronization engine for **Shopify** — built with **FastAPI**, **Celery**, **React**, **Supabase**, and **Shopify’s GraphQL API**.

This tool allows bulk CSV/Excel product uploads with intelligent **diff-and-merge** logic. Instead of blindly overwriting Shopify products, it safely updates only changed fields and supports variant grouping, SKU mapping, and realtime job progress tracking.

---

## 🚀 Features

- 📁 Upload CSV/Excel product catalogs
- 🧠 Intelligent parsing and variant grouping
- ⚡ Background task processing via Celery + Redis
- 🔄 Safe diff-and-merge Shopify synchronization
- 📊 Realtime progress tracking using Supabase
- 📦 Frontend UI for uploads and status

---

## 📦 Tech Stack

| Layer | Technology |
|-------|------------|
| API | FastAPI |
| Jobs | Celery + Redis |
| Data Parsing | Pandas |
| Frontend | React |
| Database / Realtime | Supabase |
| Shopify Integration | GraphQL Admin API |

---

## 📁 Project Structure

matrixify-lite/
├── backend/
│ ├── app/
│ │ ├── main.py # API entrypoint
│ │ ├── tasks.py # Celery worker
│ │ ├── parser.py # CSV/Excel parsing logic
│ │ ├── shopify_client.py# Shopify API logic
│ │ └── database.py # Supabase connection
│ ├── requirements.txt
│ └── .env # Secrets (not committed)
├── frontend/
│ ├── src/
│ │ ├── App.jsx # Main UI
│ │ └── lib/supabase.js # Supabase client
│ ├── package.json
│ └── vite.config.js
├── database/
│ └── schema.sql # Supabase schema
└── docker-compose.yml



---

## 🧠 How It Works

### 1. Upload

- User selects CSV/Excel file in the UI
- File is sent to backend `/import/products`
- Job is created in Supabase with status `QUEUED`
- Celery worker is triggered immediately

### 2. Background Processing

- Celery reads file from disk
- Parsing logic groups rows by `Handle`
- Variants are linked to products
- Supabase job record is updated as progress increases

### 3. Shopify Sync

For each product:

- Existing Shopify product fetched via handle
- If it exists → merge update
- If not → create new product
- Variants matched by SKU
- Only non-null fields are sent → No accidental overwrite

---

## 🔧 Setup

### Prerequisites

- Redis (for Celery)
- Supabase Project
- Shopify Admin API credentials
- Node.js + npm
- Python 3.10+

---

### Backend

1. `cd backend`
2. Create and activate virtual env
   ```bash
   python -m venv venv
   source venv/bin/activate


