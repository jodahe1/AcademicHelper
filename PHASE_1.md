## Phase 1 — Project Foundation & Database Setup

This phase establishes a reproducible, containerized foundation for the system: database (PostgreSQL + pgvector), admin tooling (pgAdmin), workflow runner (n8n), and a minimal FastAPI backend that boots and verifies DB availability.

### What we added
- Docker Compose stack with services:
  - PostgreSQL (with pgvector) for embeddings and app data
  - pgAdmin for DB management via browser
  - n8n for workflow automation (to be wired in Phase 4)
  - Backend (FastAPI) with a health endpoint and DB initialization on startup
- Database initialization script `init.sql` that creates tables, indexes, and inserts sample sources
- Backend skeleton:
  - `backend/Dockerfile` and `backend/requirements.txt`
  - `backend/main.py` with `/health` and startup hook
  - `backend/database.py` SQLAlchemy engine/session + init helpers
  - `backend/models.py` SQLAlchemy models aligned with spec
- Example env template `env.example` with all relevant variables

### Why we did it this way
- Containers give a consistent, isolated environment across machines
- `pgvector` in Postgres supports similarity search directly in SQL
- `init.sql` is idempotent on first run and sets up schema + seed data
- A minimal FastAPI app ensures the backend boots early, catching environment issues before API implementation
- pgAdmin offers quick visual verification of schema and data

### Files of interest
- `docker-compose.yml` — defines the full local stack
- `init.sql` — schema, indexes, sample data, and pgvector setup
- `backend/` — code for the FastAPI service
- `env.example` — template for .env values (do not commit your real .env)

### How to run
1) Start the stack
```
docker-compose up -d
```

2) Verify services are healthy
```
docker-compose ps
```

3) Check backend logs (should show "Application startup complete.")
```
docker-compose logs backend --tail=100
```

4) Call backend health endpoint
```
curl http://localhost:8000/health
```

5) Inspect the database schema via psql
```
docker-compose exec postgres psql -U student -d academic_helper -c "\\dt"
```

6) (Optional) Open pgAdmin
- URL: http://localhost:8080
- Login: admin@academic.com / admin123
- Add new server connection:
  - Hostname: postgres
  - Port: 5432
  - Username: student
  - Password: secure_password
  - Database: academic_helper

### Common notes & caveats
- First run downloads images; subsequent runs use cached images
- `init.sql` runs only on first initialization of the `postgres_data` volume. To force a clean re-init:
```
docker-compose down -v
docker-compose up -d
```
- If you already have local Postgres/pgAdmin installed, there is no data overwrite. Watch for host port conflicts (5432, 8080). You can change host ports in `docker-compose.yml` if needed.
- The backend container mounts your local `backend/` directory, so saving code locally triggers auto-reload in the container.

### Next (Phase 2 — Backend API)
We will implement secure endpoints:
- `POST /auth/register`, `POST /auth/login` (JWT issuance)
- `POST /upload` (file handling + job trigger)
- `GET /analysis/{id}` (retrieve results)
- `GET /sources` (RAG search)

Once Phase 2 is done, we will proceed to RAG/AI integration and n8n workflow wiring.


