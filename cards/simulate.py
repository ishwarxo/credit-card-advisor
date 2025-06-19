from services.card_logic import CardLogic

def simulate_tool(card_name, spending_habits):
    """
    Simulates annual rewards for a card based on spending habits.
    Args:
        card_name (str): Name of the card.
        spending_habits (dict): Spending amounts for fuel, travel, groceries, dining.
    Returns:
        dict: Simulated rewards or error message.
    """
    card_logic = CardLogic()
    result = card_logic.simulate_rewards(card_name, spending_habits)
    return result