# src/finance/router.py
from fastapi import APIRouter, status, Depends, BackgroundTasks
from typing import List
from src.finance.schemas import ExpenseCreate, ExpenseResponse
from src.finance.service import ExpenseService
from src.auth.dependencies import get_current_user
from src.sse_manager import sse_manager

router = APIRouter(prefix="/api/expenses", tags=["Expenses"])

@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(expense: ExpenseCreate, background_tasks: BackgroundTasks, current_user=Depends(get_current_user)):
    res = ExpenseService.create_expense(expense, user_id=current_user["user_id"])
    background_tasks.add_task(sse_manager.notify, current_user["user_id"], "update")
    return res

@router.get("/", response_model=List[ExpenseResponse])
def get_expenses(current_user=Depends(get_current_user)):
    return ExpenseService.get_all_expenses(user_id=current_user["user_id"])

@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, expense: ExpenseCreate, background_tasks: BackgroundTasks, current_user=Depends(get_current_user)):
    res = ExpenseService.update_expense(expense_id, expense, user_id=current_user["user_id"])
    background_tasks.add_task(sse_manager.notify, current_user["user_id"], "update")
    return res

@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT) 
def delete_expense(expense_id: int, background_tasks: BackgroundTasks, current_user=Depends(get_current_user)):
    ExpenseService.delete_expense(expense_id, user_id=current_user["user_id"])
    background_tasks.add_task(sse_manager.notify, current_user["user_id"], "update")
    return None