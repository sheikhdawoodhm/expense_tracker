from src.db.database import get_db_connection
from src.finance.schemas import ExpenseCreate

class ExpenseRepository:
    @staticmethod
    def save(expense: ExpenseCreate, user_id: int = 1) -> dict:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO financial_records (user_id, title, amount, type, category, description, date) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s) 
                    RETURNING id, user_id, title, amount, type, category, description, date;
                    """,
                    (
                        user_id,
                        expense.title,
                        expense.amount,
                        expense.transaction_type.value,
                        expense.category,
                        expense.description,
                        expense.transaction_date
                    )
                )
                row = cursor.fetchone()
                conn.commit()
                return {
                    "id": row[0],
                    "user_id": row[1],
                    "title": row[2],
                    "amount": float(row[3]),
                    "type": row[4],
                    "category": row[5],
                    "description": row[6],
                    "date": row[7]
                }

    @staticmethod
    def fetch_all(user_id: int = 1) -> list:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, user_id, title, amount, type, category, description, date 
                    FROM financial_records 
                    WHERE user_id = %s 
                    ORDER BY date DESC, id DESC;
                    """,
                    (user_id,)
                )
                rows = cursor.fetchall()
                return [{
                    "id": r[0],
                    "user_id": r[1],
                    "title": r[2],
                    "amount": float(r[3]),
                    "type": r[4],
                    "category": r[5],
                    "description": r[6],
                    "date": r[7]
                } for r in rows]

    @staticmethod
    def update(expense_id: int, expense: ExpenseCreate, user_id: int = 1) -> dict:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE financial_records 
                    SET title = %s, amount = %s, type = %s, category = %s, description = %s, date = %s 
                    WHERE id = %s AND user_id = %s 
                    RETURNING id, user_id, title, amount, type, category, description, date;
                    """,
                    (
                        expense.title,
                        expense.amount,
                        expense.transaction_type.value,
                        expense.category,
                        expense.description,
                        expense.transaction_date,
                        expense_id,
                        user_id
                    )
                )
                row = cursor.fetchone()
                if row is None:
                    raise ValueError("Expense not found or does not belong to the user.")
                conn.commit()
                return {
                    "id": row[0],
                    "user_id": row[1],
                    "title": row[2],
                    "amount": float(row[3]),
                    "type": row[4],
                    "category": row[5],
                    "description": row[6],
                    "date": row[7]
                }

    @staticmethod
    def delete(expense_id: int, user_id: int = 1) -> dict:
        """Deletes a financial record from the database."""
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM financial_records 
                    WHERE id = %s AND user_id = %s 
                    RETURNING id;
                    """,
                    (expense_id, user_id)
                )
                row = cursor.fetchone()
                if row is None:
                    raise ValueError("Expense not found or does not belong to the user.")
                conn.commit()
                return {"id": row[0], "status": "deleted"}