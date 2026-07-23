from pydantic import BaseModel
from typing import List

class CategoryOutlay(BaseModel):
    category: str
    totalAmount: float
    percentageOfTotalExpenses: float

class AnalyticsPayload(BaseModel):
    totalAssets: float
    totalLiabilities: float
    totalExpenses: float
    healthySpendingScore: float
    categoryWiseSpending: List[CategoryOutlay]