import json
import os

class CardLogic:
    def __init__(self):
        # Load card database (temporary; will use data/cards.json later)
        with open(os.path.join("data", "cards.json")) as f:
            self.card_db = json.load(f)

    def recommend_cards(self, user_data):
        """
        Recommends top 3–5 credit cards based on user inputs.
        Args:
            user_data (dict): Contains monthly_income, spending_habits, preferred_benefits,
                             existing_cards, credit_score.
        Returns:
            list: Top 3–5 recommended cards with name, image, reasons, and reward simulation.
        """
        monthly_income = user_data.get("monthly_income", 0)
        spending_habits = user_data.get("spending_habits", {})
        preferred_benefits = user_data.get("preferred_benefits", [])
        existing_cards = user_data.get("existing_cards", [])
        credit_score = user_data.get("credit_score", "unknown")

        # Filter cards based on credit score
        filtered_cards = self.card_db
        if credit_score != "unknown":
            min_score = int(credit_score.split("–")[0]) if "–" in credit_score else int(credit_score)
            filtered_cards = [card for card in self.card_db if card["min_credit_score"] <= min_score]
        else:
            # Assume moderate score range (650–750)
            filtered_cards = [card for card in self.card_db if card["min_credit_score"] <= 750]

        # Exclude existing cards
        filtered_cards = [card for card in filtered_cards if card["name"] not in existing_cards]

        # Calculate reward scores
        recommendations = []
        for card in filtered_cards:
            total_rewards = (
                spending_habits.get("fuel", 0) * card["rewards"]["fuel"] +
                spending_habits.get("travel", 0) * card["rewards"]["travel"] +
                spending_habits.get("groceries", 0) * card["rewards"]["groceries"] +
                spending_habits.get("dining", 0) * card["rewards"]["dining"]
            ) * 12  # Annual rewards in points
            benefit_match = len(set(card["benefits"]) & set(preferred_benefits))
            # Adjust for income (avoid high-fee cards for low income)
            fee_score = 0 if card["annual_fee"] <= (monthly_income * 0.1) else -1000
            score = total_rewards + (benefit_match * 1000) - card["annual_fee"]

            recommendations.append({
                "card": card,
                "score": score,
                "total_rewards": total_rewards / 100  # Convert points to INR (simplified)
            })

        # Sort and select top 3–5
        recommendations = sorted(recommendations, key=lambda x: x["score"], reverse=True)[:3]

        # Format output
        output = []
        for rec in recommendations:
            card = rec["card"]
            reasons = [
                f"Matches your preference for {', '.join(set(card['benefits']) & set(preferred_benefits)) or 'multiple benefits'}",
                f"High rewards on {max(card['rewards'], key=card['rewards'].get)} spending"
            ]
            if credit_score == "unknown":
                reasons.append("Assumes a moderate credit score (650–750)")

            output.append({
                "name": card["name"],
                "image": card["image"],
                "reasons": reasons,
                "reward": f"You could earn Rs. {int(rec['total_rewards'])}/year in rewards."
            })

        return output

    def lookup_card(self, card_name):
        """
        Looks up details for a specific card.
        Args:
            card_name (str): Name of the card to look up.
        Returns:
            dict: Card details or None if not found.
        """
        for card in self.card_db:
            if card["name"].lower() == card_name.lower():
                return card
        return None

    def count_cards(self):
        """
        Returns the total number of cards in the database.
        Returns:
            int: Number of cards.
        """
        return len(self.card_db)

    def compare_cards(self, card_name1, card_name2):
        """
        Compares two cards by benefits, rewards, and fees.
        Args:
            card_name1 (str): First card name.
            card_name2 (str): Second card name.
        Returns:
            dict: Comparison details or error message.
        """
        card1 = self.lookup_card(card_name1)
        card2 = self.lookup_card(card_name2)
        if not card1 or not card2:
            return {"error": "One or both cards not found."}

        comparison = {
            "card1": card1["name"],
            "card2": card2["name"],
            "benefits": {
                card1["name"]: card1["benefits"],
                card2["name"]: card2["benefits"],
            },
            "rewards": {
                card1["name"]: card1["rewards"],
                card2["name"]: card2["rewards"],
            },
            "annual_fees": {
                card1["name"]: card1["annual_fee"],
                card2["name"]: card2["annual_fee"],
            }
        }
        return comparison

    def simulate_rewards(self, card_name, spending_habits):
        """
        Simulates annual rewards for a card based on spending habits.
        Args:
            card_name (str): Name of the card.
            spending_habits (dict): Spending amounts for fuel, travel, groceries, dining.
        Returns:
            dict: Simulated rewards or error message.
        """
        card = self.lookup_card(card_name)
        if not card:
            return {"error": "Card not found."}

        total_rewards = (
            spending_habits.get("fuel", 0) * card["rewards"]["fuel"] +
            spending_habits.get("travel", 0) * card["rewards"]["travel"] +
            spending_habits.get("groceries", 0) * card["rewards"]["groceries"] +
            spending_habits.get("dining", 0) * card["rewards"]["dining"]
        ) * 12  # Annual rewards
        return {
            "card_name": card["name"],
            "annual_rewards": f"Rs. {int(total_rewards / 100)}"  # Convert points to INR
        }