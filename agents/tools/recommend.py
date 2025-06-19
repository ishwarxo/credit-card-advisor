from services.card_logic import CardLogic

def recommend_tool(user_data):
    """
    Recommends 3–5 credit cards based on user inputs.
    Args:
        user_data (dict): Contains monthly_income, spending_habits, preferred_benefits,
                         existing_cards, credit_score.
    Returns:
        dict: List of recommended cards with name, image, reasons, and reward simulation.
    """
    card_logic = CardLogic()
    recommendations = card_logic.recommend_cards(user_data)
    return {
        "recommendations": recommendations
    }