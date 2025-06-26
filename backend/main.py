from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SimpleMediaSocial", version="0.1.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from routers import auth, users, posts, interactions, admin, me

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(interactions.router, prefix="/interactions", tags=["interactions"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(me.router, prefix="/me", tags=["me"])

@app.get("/")
async def root():
    return {"message": "SimpleMediaSocial API"}
