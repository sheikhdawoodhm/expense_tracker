from src.db.tableCreation import get_db_connection
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
    def get_raw_category_sums(user_id: int) -> List[Dict[str, Any]]:
        """Queries raw total spend grouped by category."""
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT category, COALESCE(SUM(amount), 0) as total_amount
                    FROM financial_records
                    WHERE user_id = %s AND type = 'expense'
                    GROUP BY category
                    ORDER BY total_amount DESC;
                    """,
                    (user_id,)
                )
                rows = cursor.fetchall()
                return [{"category": row[0], "totalAmount": float(row[1])} for row in rows]