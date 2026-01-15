import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User
from auth import create_access_token, hash_password
from jose import jwt

# Setup
DATABASE_URL = "sqlite:///./techtalk.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Test 1: Check if user exists
user = db.query(User).filter(User.id == 1).first()
print(f"User exists: {user is not None}")
if user:
    print(f"Username: {user.username}")

# Test 2: Create token
token = create_access_token({"sub": 1})
print(f"Token created: {token[:50]}...")

# Test 3: Decode token
SECRET_KEY = "your-secret-key-change-in-production"
try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    print(f"Token decoded successfully: {payload}")
    user_id = payload.get("sub")
    print(f"User ID from token: {user_id}, Type: {type(user_id)}")
    
    # Test 4: Query user with decoded ID
    user2 = db.query(User).filter(User.id == user_id).first()
    print(f"User found with decoded ID: {user2 is not None}")
except Exception as e:
    print(f"Error: {e}")

db.close()
