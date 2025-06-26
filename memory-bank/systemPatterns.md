# SimpleMediaSocial System Patterns

## Architecture
- REST API design
- Layered architecture:
  - Routes (FastAPI endpoints)
  - Services (business logic)
  - Models (database models)
  - Database (SQLite)

## Key Technical Decisions
- Use FastAPI for async capabilities
- SQLite for development with PostgreSQL compatibility
- JSON field implementation that works across databases
- Pydantic for data validation  
- PyJWT for authentication

## Design Patterns
- Repository pattern for database access  
- Dependency injection for services
- Factory pattern for test data
- Cross-database JSON field implementation

## Component Relationships
- Users can create multiple Posts
- Users can follow other Users
- Posts can be liked by multiple Users
- Posts can be shared by multiple Users
- Posts can be replied to (parent-child relationships)
- Posts maintain engagement counts (likes, shares, replies)
- Users have JSON attributes for flexible metadata
