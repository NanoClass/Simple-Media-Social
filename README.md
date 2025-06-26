# SimpleMediaSocial API

A Twitter/X-like social media API built with Python FastAPI and SQLite.

## Features

### Core Functionality
- User registration and authentication (JWT)
- Post creation with content validation
- Post replies with threading
- Like/unlike posts
- Share posts
- Follow/unfollow users

### Advanced Features
- JSONB user attributes for flexible metadata storage
- Timestamp tracking (created_at, updated_at, modified_at)
- Paginated responses for posts and replies
- Admin approval system for new users

## API Documentation

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get access token

### Posts
- `POST /posts` - Create new post
- `GET /posts/{id}` - Get post with replies
- `PATCH /posts/{id}` - Update post content
- `GET /posts/user/{username}` - Get user's posts

### Interactions
- `POST /interactions/{post_id}/like` - Like a post
- `POST /interactions/{post_id}/reply` - Reply to post  
- `POST /interactions/{post_id}/share` - Share post
- `POST /interactions/{user_id}/follow` - Follow user

### User Management
- `GET /users/me` - Get current user profile
- `PATCH /users/me/attributes` - Update user attributes

## Getting Started

### Prerequisites
- Python 3.10+
- SQLite

### Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize database:
   ```bash
   python -c "from database import init_db; init_db()"
   ```

### Running the API
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000` with interactive docs at `http://localhost:8000/docs`

## Project Structure
```
.
├── backend/            # Python FastAPI
│   ├── main.py         # App entry point  
│   ├── models/         # Database models
│   ├── routers/        # API endpoints
│   ├── schemas/        # Pydantic models
│   ├── services/       # Business logic
│   ├── database.py     # Database setup
│   ├── config.py       # Configuration
│   └── Dockerfile      # Backend Docker config
├── frontend/           # Future frontend
├── memory-bank/        # Project documentation
├── docker-compose.yml  # Orchestration
└── README.md           # Project overview
```

## License
MIT
