from src.finance.repository import AnalyticsRepository
from src.finance.schemas import AnalyticsPayload, CategoryOutlay

class AnalyticsService:
    @staticmethod
    def calculate_user_analytics(user_id: int) -> AnalyticsPayload:
        # 1. Fetch raw totals from Repository
        assets, liabilities, expenses = AnalyticsRepository.get_raw_type_sums(user_id)
        
        # 2. Calculate Healthy Spending Score (Business Rule)
        if expenses == 0:
            healthy_score = 100.0
        elif assets == 0:
            healthy_score = 0.0
        else:
            # Score scales based on how much buffer assets provide over expenses
            ratio = assets / (assets + expenses)
            healthy_score = round(ratio * 100, 1)

        # 3. Fetch raw category breakdowns
        raw_categories = AnalyticsRepository.get_raw_category_sums(user_id)
        
        # 4. Map and calculate percentages for each category
        processed_categories = []
        for cat in raw_categories:
            percentage = 0.0
            if expenses > 0:
                percentage = round((cat["totalAmount"] / expenses) * 100, 1)
                
            processed_categories.append(
                CategoryOutlay(
                    category=cat["category"],
                    totalAmount=cat["totalAmount"],
                    percentageOfTotalExpenses=percentage
                )
            )

        # 5. Return clean structured payload matching our schema
        return AnalyticsPayload(
            totalAssets=assets,
            totalLiabilities=liabilities,
            totalExpenses=expenses,
            healthySpendingScore=healthy_score,
            categoryWiseSpending=processed_categories
        )