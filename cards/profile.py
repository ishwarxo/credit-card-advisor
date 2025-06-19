def profile_tool(user_data):
    """
    Stores user profile data from the conversation.
    Args:
        user_data (dict): User inputs (e.g., monthly_income, spending_habits).
    Returns:
        dict: Confirmation of profile update.
    """
    # Note: Profile is stored in-memory in base_agent.py; this tool just confirms
    return {"status": "Profile updated successfully"}