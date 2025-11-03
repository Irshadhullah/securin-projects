```markdown
# Securin Projects — Recipes API

This repo contains a FastAPI service that loads `data/recipes.json`, normalizes records, stores recipes into PostgreSQL (nutrients as JSONB), and exposes:
- GET /api/recipes — paginated, sorted by rating desc
- GET /api/recipes/search — field-level searching (title, cuisine, rating comparators, total_time, calories)

See app/ for source and docker-compose.yml to run app + postgres.

Quick start:
1. Place your provided recipes.json in `/data/recipes.json`.
2. Copy .env.example (if used) and edit DB credentials.
3. docker-compose up --build
4. After DB is ready:
   docker-compose exec web python /app/seed.py

API docs:
- http://localhost:8000/docs (when running)
```