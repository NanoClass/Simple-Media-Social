# SimpleMediaSocial Tech Context

## Technologies Used
- Python 3.10+
- FastAPI 
- SQLite (with PostgreSQL compatibility)
- Pydantic
- PyJWT
- Uvicorn (ASGI server)
- SQLAlchemy with JSON/JSONB support

## Development Setup
1. Docker-based development environment
2. Project structure:
   - backend/ (Python FastAPI)
     - main.py (entry point)
     - routers/ (API endpoints)
     - models/ (database models)
     - schemas/ (Pydantic models)
     - services/ (business logic)
   - frontend/ (Future React/Vue frontend)
   - memory-bank/ (Documentation)
3. Docker Compose for orchestration

## Technical Constraints
- SQLite database for development (PostgreSQL compatible)
- JSON field implementation works across SQLite and PostgreSQL
- No frontend implementation (API only)
- JWT authentication with refresh tokens
- Timestamp tracking for all modifications (created_at, updated_at, modified_at)

## Dependencies
- fastapi
- uvicorn
- PyJWT
- bcrypt (hashing)
- sqlalchemy (ORM)
- pytest (testing)
- python-multipart (form data)
