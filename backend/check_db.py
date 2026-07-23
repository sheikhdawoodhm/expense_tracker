from dotenv import load_dotenv
load_dotenv()
from src.db.database import get_db_connection
with get_db_connection() as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT id, email FROM users")
        print("Users:", cur.fetchall())
        cur.execute("SELECT id, user_id, amount, type FROM financial_records")
        print("Records:", cur.fetchall())
        cur.execute("SELECT id, user_id, title FROM financial_goals")
        print("Goals:", cur.fetchall())
