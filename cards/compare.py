from services.card_logic import CardLogic

def compare_tool(card_name1, card_name2):
    """
    Compares two credit cards by benefits, rewards, and fees.
    Args:
        card_name1 (str): First card name.
        card_name2 (str): Second card name.
    Returns:
        dict: Comparison details or error message.
    """
    card_logic = CardLogic()
    result = card_logic.compare_cards(card_name1, card_name2)
    return result