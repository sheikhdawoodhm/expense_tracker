from pydantic import BaseModel, Field, ConfigDict
import datetime
from typing import Optional
from enum import Enum

class TransactionType(str, Enum):
    EXPENSE = "expense"
    ASSET = "asset"
    LIABILITY = "liability"

class ExpenseCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    amount: float = Field(..., gt=0)
    transaction_type: TransactionType = Field(..., validation_alias="type", serialization_alias="type")
    category: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(None)
    

    transaction_date: datetime.date = Field(
        default_factory=datetime.date.today, 
        validation_alias="date", 
        serialization_alias="date"
    )

class ExpenseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    user_id: int
    amount: float
    transaction_type: TransactionType = Field(..., validation_alias="type", serialization_alias="type")
    category: str
    description: Optional[str] = None
    transaction_date: datetime.date = Field(..., validation_alias="date", serialization_alias="date")