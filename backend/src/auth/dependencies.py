import os
from fastapi import Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from psycopg2.extras import RealDictCursor
from src.db.database import get_db_connection
import jwt

SECRET_KEY = os.getenv("JWT_SECRET", "supersecretkey")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def verify_token_and_session(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        session_id = payload.get("session_id")
        if user_id is None or session_id is None:
            raise credentials_exception
        
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT is_active FROM sessions WHERE id = %s", (session_id,))
                session = cur.fetchone()
                if not session or not session["is_active"]:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session revoked")
                    
        return {"user_id": int(user_id), "session_id": session_id}
    except jwt.PyJWTError:
        raise credentials_exception

def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token_and_session(token)

def get_current_user_sse(token: str = Query(...)):
    return verify_token_and_session(token)
