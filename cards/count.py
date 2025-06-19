from services.card_logic import CardLogic

def count_tool():
    """
    Returns the total number of credit cards in the database.
    Returns:
        dict: Number of cards.
    """
    card_logic = CardLogic()
    count = card_logic.count_cards()
    return {"count": count}