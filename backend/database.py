from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base, User

SQLALCHEMY_DATABASE_URL = "sqlite:///./social.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
    
    # Create admin user if doesn't exist
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            from services.auth import get_password_hash
            admin = User(
                username="admin",
                email="admin@example.com",
                password_hash=get_password_hash("supersecure123"),
                is_admin=True,
                attributes={}
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()
