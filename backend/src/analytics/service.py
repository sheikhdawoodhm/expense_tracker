from src.analytics.query import AnalyticsRepository
from src.analytics.schemas import AnalyticsPayload, CategoryOutlay

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

        # Calculate Net Worth
        net_worth = assets - liabilities

        # 3. Fetch raw category breakdowns
        raw_categories = AnalyticsRepository.get_raw_category_sums(user_id)
        
        # 4. Map and calculate percentages for each category
        processed_categories = []
        for cat in raw_categories:
            percentage = 0.0
            amount_float = float(cat["totalAmount"])
            if expenses > 0:
                percentage = round((amount_float / expenses) * 100, 1)
                
            processed_categories.append(
                CategoryOutlay(
                    category=cat["category"],
                    totalAmount=amount_float,
                    percentageOfTotalExpenses=percentage
                )
            )

        # 5. Fetch Goal Settings
        goal = AnalyticsRepository.get_latest_goal(user_id)
        from src.analytics.schemas import GoalSettings
        if goal:
            settings = GoalSettings(
                goalName=goal["title"],
                goalTargetAmount=goal["target_threshold"],
                monthlySavingsContribution=goal["monthly_contribution"]
            )
        else:
            settings = GoalSettings(
                goalName="Emergency Fund Cushion",
                goalTargetAmount=50000,
                monthlySavingsContribution=2500
            )

        # 6. Calculate Ring Stroke Offset (for UI)
        # Assuming circumference is 251.32. A score of 100 means full circle (offset 0)
        # Score of 0 means empty circle (offset 251.32)
        circumference = 251.32
        ring_offset = circumference - (healthy_score / 100.0) * circumference

        # 7. Return clean structured payload matching our schema
        return AnalyticsPayload(
            totalAssets=assets,
            totalLiabilities=liabilities,
            totalExpenses=expenses,
            netWorth=net_worth,
            healthySpendingScore=healthy_score,
            ringStrokeOffset=ring_offset,
            categoryWiseSpending=processed_categories,
            settings=settings
        )

    @staticmethod
    def save_user_goal(user_id: int, settings: 'GoalSettings') -> 'GoalSettings':
        AnalyticsRepository.save_goal(
            user_id=user_id,
            title=settings.goalName,
            target_threshold=settings.goalTargetAmount,
            monthly_contribution=settings.monthlySavingsContribution
        )
        return settings