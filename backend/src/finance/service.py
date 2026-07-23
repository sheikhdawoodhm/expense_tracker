from src.finance.query import ExpenseRepository
from src.finance.schemas import ExpenseCreate

class ExpenseService:
    @staticmethod
    def create_expense(expense: ExpenseCreate, user_id: int = 1) -> dict:
        expense.category = expense.category.strip().title()
        return ExpenseRepository.save(expense, user_id)

    @staticmethod
    def get_all_expenses(user_id: int = 1) -> list:
        return ExpenseRepository.fetch_all(user_id)

    @staticmethod
    def update_expense(expense_id: int, expense: ExpenseCreate, user_id: int = 1) -> dict:
        return ExpenseRepository.update(expense_id, expense, user_id)

    @staticmethod
    def delete_expense(expense_id: int, user_id: int = 1):
        return ExpenseRepository.delete(expense_id, user_id)