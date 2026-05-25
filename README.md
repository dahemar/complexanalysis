# Complex Analysis Visualizer

A minimal full-stack prototype for visualizing complex analysis problems. The **Python** backend performs the math; the **Astro** frontend renders results on the **Argand plane**.

Current feature: **addition of two complex numbers**.

## Project layout

```
backend/     FastAPI + Python (complex arithmetic)
frontend/    Astro (UI + Argand SVG plot)
```

## Prerequisites

- Python 3.11+
- Node.js 20+

## Quick start

### 1. Backend (port 8000)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

API docs: http://127.0.0.1:8000/docs

### 2. Frontend (port 4321)

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:4321 — the dev server proxies `/api` and `/health` to the backend.

## API

`POST /api/complex/add`

```json
{
  "a": { "real": 2, "imag": 1 },
  "b": { "real": -1, "imag": 2 }
}
```

Response:

```json
{
  "a": { "real": 2, "imag": 1 },
  "b": { "real": -1, "imag": 2 },
  "sum": { "real": 1, "imag": 3 }
}
```

## Next steps

- Multiplication, conjugate, polar form
- Contour plots and holomorphic maps
- Shared types / OpenAPI client generation
