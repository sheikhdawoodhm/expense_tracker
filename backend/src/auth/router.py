from fastapi import APIRouter, Depends, HTTPException, status
from psycopg2.extras import RealDictCursor
import uuid
from datetime import datetime, timedelta
from src.auth.schemas import UserCreate, UserLogin, Token, RefreshTokenRequest
from src.auth.service import get_password_hash, verify_password, create_access_token, create_refresh_token, REFRESH_TOKEN_EXPIRE_DAYS, SECRET_KEY, ALGORITHM
from src.db.database import get_db_connection
from src.auth.dependencies import get_current_user
import jwt

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
            
            # Simple direct response, user can login immediately afterwards
            return {"user": new_user, "message": "Signup successful"}

@router.post("/login", response_model=Token)
def login(user: UserLogin):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE email = %s", (user.email,))
            db_user = cur.fetchone()
            if not db_user or not verify_password(user.password, db_user["hashed_password"]):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
            
            session_id = str(uuid.uuid4())
            access_token = create_access_token(data={"sub": str(db_user["id"]), "session_id": session_id})
            refresh_token = create_refresh_token(data={"sub": str(db_user["id"]), "session_id": session_id})
            
            expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
            
            cur.execute(
                "INSERT INTO sessions (id, user_id, refresh_token, expires_at) VALUES (%s, %s, %s, %s)",
                (session_id, db_user["id"], refresh_token, expires_at)
            )
            conn.commit()

            return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh", response_model=Token)
def refresh_token(request: RefreshTokenRequest):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(request.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        session_id = payload.get("session_id")
        if user_id is None or session_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT is_active FROM sessions WHERE id = %s", (session_id,))
            session = cur.fetchone()
            if not session or not session["is_active"]:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session revoked")
            
            # Generate fresh access token only
            access_token = create_access_token(data={"sub": str(user_id), "session_id": session_id})
            return {"access_token": access_token, "refresh_token": request.refresh_token, "token_type": "bearer"}

@router.post("/logout")
def logout(current_user=Depends(get_current_user)):
    session_id = current_user.get("session_id")
    if session_id:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE sessions SET is_active = FALSE WHERE id = %s", (session_id,))
                conn.commit()
    return {"message": "Successfully logged out"}
