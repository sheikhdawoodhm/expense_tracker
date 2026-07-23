from pydantic import BaseModel
from typing import List

class CategoryOutlay(BaseModel):
    category: str
    totalAmount: float
    percentageOfTotalExpenses: float

class GoalSettings(BaseModel):
    goalName: str
    goalTargetAmount: float
    monthlySavingsContribution: float

class AnalyticsPayload(BaseModel):
    totalAssets: float
    totalLiabilities: float
    totalExpenses: float
    netWorth: float
    healthySpendingScore: float
    ringStrokeOffset: float
    categoryWiseSpending: List[CategoryOutlay]
    settings: GoalSettings