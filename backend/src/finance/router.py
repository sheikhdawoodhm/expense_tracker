# src/finance/router.py
from fastapi import APIRouter, status
from typing import List
from src.finance.schemas import ExpenseCreate, ExpenseResponse
from src.finance.service import ExpenseService

router = APIRouter(prefix="/api/expenses", tags=["Expenses"])

@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(expense: ExpenseCreate):
    return ExpenseService.create_expense(expense, user_id=1)

@router.get("/", response_model=List[ExpenseResponse])
def get_expenses():
    return ExpenseService.get_all_expenses(user_id=1)

@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, expense: ExpenseCreate):
    return ExpenseService.update_expense(expense_id, expense, user_id=1)

@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT) 
def delete_expense(expense_id: int):
    ExpenseService.delete_expense(expense_id, user_id=1)
    return None