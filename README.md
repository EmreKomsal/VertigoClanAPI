
# VertigoClanAPI

A FastAPI-powered backend API to manage and explore clan data. It supports CRUD operations, CSV import/export, filtering, and cloud deployment via Docker and Google Cloud Run.

---

## 🔧 Features

- Create, list, retrieve, and delete clans
- Filter clans by region and sort by creation time
- Upload clan data via CSV (`clan_sample_data.csv`)
- Export clans to CSV
- RESTful API built with **FastAPI**
- Uses **PostgreSQL** (Cloud SQL-ready)
- Deployed with **Docker** + **Cloud Run**
- Pydantic v2 compatible

---

## 📁 Project Structure

```
VertigoClanAPI/
│
├── app/
│   ├── main.py          # FastAPI app
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── crud.py          # DB operations
│   └── database.py      # DB connection config
│
├── clan_sample_data.csv # Example CSV to import
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container setup
└── README.md            # Project documentation
```

---

## 🚀 Local Development

### 1. Setup virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start PostgreSQL (if running locally)

```bash
docker run --name local-db -e POSTGRES_USER=<user> -e POSTGRES_PASSWORD=<pass> -e POSTGRES_DB=clandb -p 5432:5432 -d postgres
```

Update the `DATABASE_URL` in `.env` or `app/database.py`.

### 3. Run the app

```bash
uvicorn app.main:app --reload
```

---

## 🐳 Docker Development

```bash
docker build -t clan-api .
docker run -p 8000:8080 --env DATABASE_URL=<your_connection_url> clan-api
```

---

## ☁️ Deploy to Google Cloud Run

### 1. Enable required APIs

```bash
gcloud services enable run.googleapis.com sqladmin.googleapis.com artifactregistry.googleapis.com
```

### 2. Create Artifact Registry

```bash
gcloud artifacts repositories create clan-api-repo \
  --repository-format=docker \
  --location=<region> \
  --description="Clan API repo"
```

### 3. Build & Push the Docker Image

```bash
docker build -t <region>-docker.pkg.dev/<your-project-id>/clan-api-repo/clan-api .
gcloud auth configure-docker <region>-docker.pkg.dev
docker push <region>-docker.pkg.dev/<your-project-id>/clan-api-repo/clan-api
```

### 4. Create VPC Connector (only once)

```bash
gcloud compute networks vpc-access connectors create run-vpc-connector \
  --region=<region> \
  --range=10.8.0.0/28
```

### 5. Deploy to Cloud Run

```bash
gcloud run deploy clan-api \
  --image=<region>-docker.pkg.dev/<your-project-id>/clan-api-repo/clan-api \
  --platform=managed \
  --region=<region> \
  --allow-unauthenticated \
  --vpc-connector=run-vpc-connector \
  --add-cloudsql-instances=<project>:<region>:<instance> \
  --set-env-vars="DATABASE_URL=postgresql+psycopg2://<user>:<pass>@/clandb?host=/cloudsql/<project>:<region>:<instance>"
```

---

## 📡 API Endpoints

| Method | Endpoint               | Description                        |
|--------|------------------------|------------------------------------|
| GET    | `/clans`               | List clans (filter/sort optional) |
| POST   | `/clans`               | Create a new clan                  |
| GET    | `/clans/{clan_id}`     | Get clan by ID                     |
| DELETE | `/clans/{clan_id}`     | Delete a clan                      |
| POST   | `/upload_csv`          | Import clans from CSV              |
| GET    | `/clans/export_csv`    | Export clans to CSV                |

---

## ✅ Environment Variables

| Name          | Description                          |
|---------------|--------------------------------------|
| `DATABASE_URL`| SQLAlchemy connection string (Cloud SQL or local PostgreSQL) |

Use `.env` or pass manually at runtime.

---

## 📜 License

MIT License