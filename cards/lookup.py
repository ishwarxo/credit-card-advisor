from services.card_logic import CardLogic

def lookup_tool(card_name):
    """
    Looks up details for a specific credit card.
    Args:
        card_name (str): Name of the card to look up.
    Returns:
        dict: Card details or error message.
    """
    card_logic = CardLogic()
    result = card_logic.lookup_card(card_name)
    if result:
        return result
    return {"error": f"Card '{card_name}' not found."}