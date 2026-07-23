from src.db.database import get_db_connection
from psycopg2.extras import RealDictCursor
from typing import List, Tuple, Dict, Any

class AnalyticsRepository:
    @staticmethod
    def get_raw_type_sums(user_id: int) -> Tuple[float, float, float]:
        """Queries the raw sums of assets, liabilities, and expenses."""
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT 
                        COALESCE(SUM(CASE WHEN type = 'asset' THEN amount ELSE 0 END), 0) as assets,
                        COALESCE(SUM(CASE WHEN type = 'liability' THEN amount ELSE 0 END), 0) as liabilities,
                        COALESCE(SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END), 0) as expenses
                    FROM financial_records
                    WHERE user_id = %s;
                    """,
                    (user_id,)
                )
                assets, liabilities, expenses = cursor.fetchone()
                return float(assets), float(liabilities), float(expenses)

    @staticmethod
    def get_raw_category_sums(user_id: int) -> list:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT category, SUM(amount) as "totalAmount"
                    FROM financial_records
                    WHERE user_id = %s AND type = 'expense'
                    GROUP BY category
                    ORDER BY "totalAmount" DESC
                """, (user_id,))
                return cursor.fetchall()

    @staticmethod
    def get_latest_goal(user_id: int) -> dict:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT title, target_threshold, monthly_contribution, estimated_horizon_months, category, is_completed
                    FROM financial_goals
                    WHERE user_id = %s
                    ORDER BY id DESC
                    LIMIT 1
                """, (user_id,))
                return cursor.fetchone()

    @staticmethod
    def save_goal(user_id: int, title: str, target_threshold: float, monthly_contribution: float) -> dict:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO financial_goals (user_id, title, target_threshold, monthly_contribution, estimated_horizon_months, category, is_completed)
                    VALUES (%s, %s, %s, %s, 0, 'General', FALSE)
                    RETURNING id, title, target_threshold, monthly_contribution
                """, (user_id, title, target_threshold, monthly_contribution))
                row = cursor.fetchone()
                conn.commit()
                return row