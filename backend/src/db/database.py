import os
from contextlib import contextmanager
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)

try:
    db_pool = SimpleConnectionPool(1, 10, dsn=DATABASE_URL)
    print("Database connection pool initialized.")
except Exception as e:
    print(f" Failed to initialize database pool: {e}")
    db_pool = None

@contextmanager
def get_db_connection():
    if db_pool is None:
        raise RuntimeError("Database connection pool is offline.")
    
    connection = db_pool.getconn()
    try:
        yield connection
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        db_pool.putconn(connection)

def init_db():
    users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        hashed_password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    records_table = """
    CREATE TABLE IF NOT EXISTS financial_records (
        id SERIAL PRIMARY KEY,
        user_id INT NOT NULL,
        amount NUMERIC(12, 2) NOT NULL,
        type VARCHAR(30) NOT NULL CHECK (type IN ('expense', 'asset', 'liability')),
        category VARCHAR(100) NOT NULL,
        description TEXT,
        date DATE NOT NULL,
        CONSTRAINT fk_user_records FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """

    goals_table = """
    CREATE TABLE IF NOT EXISTS financial_goals (
        id SERIAL PRIMARY KEY,
        user_id INT NOT NULL,
        title VARCHAR(150) NOT NULL,
        target_threshold NUMERIC(12, 2) NOT NULL,
        monthly_contribution NUMERIC(12, 2) NOT NULL,
        estimated_horizon_months NUMERIC(5, 1) NOT NULL,
        category VARCHAR(100) NOT NULL,
        is_completed BOOLEAN DEFAULT FALSE,
        CONSTRAINT fk_user_goals FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """

    sessions_table = """
    CREATE TABLE IF NOT EXISTS sessions (
        id VARCHAR(36) PRIMARY KEY,
        user_id INT NOT NULL,
        refresh_token VARCHAR(512) NOT NULL,
        expires_at TIMESTAMP NOT NULL,
        is_active BOOLEAN DEFAULT TRUE,
        CONSTRAINT fk_user_sessions FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """

    print("Syncing database structure...")
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(users_table)
            cursor.execute(records_table)
            cursor.execute(goals_table)
            cursor.execute(sessions_table)
            conn.commit()
    print(" Database verification complete.")