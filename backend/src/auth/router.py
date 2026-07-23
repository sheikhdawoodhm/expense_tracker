from fastapi import APIRouter, Depends, HTTPException, status
from psycopg2.extras import RealDictCursor
from src.auth.schemas import UserCreate, UserLogin, Token
from src.auth.service import get_password_hash, verify_password, create_access_token
from src.db.database import get_db_connection

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/signup")
def signup(user: UserCreate):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT id FROM users WHERE email = %s", (user.email,))
            if cur.fetchone():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
            
            hashed_pw = get_password_hash(user.password)
            cur.execute(
                "INSERT INTO users (email, hashed_password) VALUES (%s, %s) RETURNING id, email",
                (user.email, hashed_pw)
            )
            new_user = cur.fetchone()
            conn.commit()
            
            access_token = create_access_token(data={"sub": str(new_user["id"])})
            return {"access_token": access_token, "token_type": "bearer", "user": new_user}

@router.post("/login", response_model=Token)
def login(user: UserLogin):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE email = %s", (user.email,))
            db_user = cur.fetchone()
            if not db_user or not verify_password(user.password, db_user["hashed_password"]):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
            
            access_token = create_access_token(data={"sub": str(db_user["id"])})
            return {"access_token": access_token, "token_type": "bearer"}
