from openai import OpenAI
import json
import os
from dotenv import load_dotenv
from services.card_logic import CardLogic

# Load environment variables
load_dotenv()

class CreditCardAssistant:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.card_logic = CardLogic()
        self.user_data = {}  # Store user inputs (e.g., income, spending habits)
        
        # Create the Assistant
        self.assistant = self.client.beta.assistants.create(
            name="Credit Card Recommender",
            instructions="""
You are a credit card recommendation assistant for users in India. Your goal is to collect user information through a dynamic, conversational dialogue and provide personalized credit card recommendations or perform related tasks (e.g., card lookup, comparison, reward simulation). Follow these steps:

1. **Collect User Inputs**:
   - Ask one question at a time to gather:
     - Monthly income (in INR, e.g., 50,000).
     - Monthly spending habits (fuel, travel, groceries, dining in INR).
     - Preferred benefits (choose from cashback, travel_points, lounge_access).
     - Existing credit cards (optional, ask for card names or 'none').
     - Approximate credit score (e.g., 700–850, or allow 'unknown').
   - Store responses in context to avoid repetition (use self.user_data).
   - Use a friendly, professional tone and confirm each input (e.g., "Got it, your monthly income is Rs. 50,000. Now, how much do you spend on groceries monthly?").
   - If a user skips a question or provides unclear input, gently rephrase and ask again.
   - Once all inputs are collected, call the 'recommend' tool unless the user requests a specific action (e.g., compare cards).

2. **Handle User Requests**:
   - If the user asks for recommendations, call the 'recommend' tool with collected inputs.
   - If the user asks about a specific card, use the 'lookup' tool.
   - If the user wants to compare cards, use the 'compare' tool.
   - If the user asks for reward simulation, use the 'simulate' tool.
   - If the user asks how many cards are available, use the 'count' tool.
   - Store user inputs using the 'profile' tool for context.

3. **Response Formatting**:
   - For recommendations, present 3–5 cards with:
     - Card name
     - Image URL
     - Key reasons for recommendation
     - Rewards (e.g., "You could earn Rs. 8,000/year cashback").
   - For other tasks, format responses clearly and concisely.
   - Use INR for all financial calculations.
   - If credit score is 'unknown', note it assumes a 650–750 range.
   - After presenting recommendations, ask: "Would you like to compare any of these cards (e.g., 'Compare HDFC Infinia and Amex Platinum')?"

4. **Error Handling**:
   - If inputs are invalid (e.g., negative income), prompt for correction.
   - If a tool call fails, inform the user politely and suggest rechecking inputs.

5. **Follow-Up**:
   - After responding, ask if the user wants to adjust preferences, explore more cards, or perform another task (e.g., compare cards).

**Constraints**:
- Use INR for all financial values.
- Do not store user data outside the conversation context.
- Maintain a conversational, engaging tone.
- Assume a database of Indian credit cards is accessible via tools.
""",
            model="gpt-4o-mini",
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "recommend",
                        "description": "Recommends 3–5 credit cards based on user inputs.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "monthly_income": {"type": "integer", "description": "Monthly income in INR"},
                                "spending_habits": {
                                    "type": "object",
                                    "properties": {
                                        "fuel": {"type": "integer", "description": "Monthly fuel spending in INR"},
                                        "travel": {"type": "integer", "description": "Monthly travel spending in INR"},
                                        "groceries": {"type": "integer", "description": "Monthly groceries spending in INR"},
                                        "dining": {"type": "integer", "description": "Monthly dining spending in INR"},
                                    },
                                    "required": ["fuel", "travel", "groceries", "dining"],
                                },
                                "preferred_benefits": {
                                    "type": "array",
                                    "items": {"type": "string", "enum": ["cashback", "travel_points", "lounge_access"]},
                                    "description": "Preferred card benefits",
                                },
                                "existing_cards": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "List of existing credit card names or 'none'"
                                },
                                "credit_score": {
                                    "type": "string",
                                    "description": "Approximate credit score (e.g., '700–800') or 'unknown'"
                                },
                            },
                            "required": ["monthly_income", "spending_habits", "preferred_benefits"],
                        },
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "lookup",
                        "description": "Looks up details for a specific credit card.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "card_name": {"type": "string", "description": "Name of the card to look up"}
                            },
                            "required": ["card_name"],
                        },
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "count",
                        "description": "Returns the total number of cards in the database.",
                        "parameters": {"type": "object", "properties": {}},
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "profile",
                        "description": "Stores user profile data from the conversation.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "monthly_income": {"type": "integer", "description": "Monthly income in INR"},
                                "spending_habits": {
                                    "type": "object",
                                    "properties": {
                                        "fuel": {"type": "integer", "description": "Monthly fuel spending in INR"},
                                        "travel": {"type": "integer", "description": "Monthly travel spending in INR"},
                                        "groceries": {"type": "integer", "description": "Monthly groceries spending in INR"},
                                        "dining": {"type": "integer", "description": "Monthly dining spending in INR"},
                                    },
                                },
                                "preferred_benefits": {
                                    "type": "array",
                                    "items": {"type": "string", "enum": ["cashback", "travel_points", "lounge_access"]},
                                },
                                "existing_cards": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                },
                                "credit_score": {"type": "string"},
                            },
                        },
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "compare",
                        "description": "Compares two credit cards by benefits, rewards, and fees.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "card_name1": {"type": "string", "description": "First card name"},
                                "card_name2": {"type": "string", "description": "Second card name"},
                            },
                            "required": ["card_name1", "card_name2"],
                        },
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "simulate",
                        "description": "Simulates annual rewards for a card based on spending habits.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "card_name": {"type": "string", "description": "Name of the card"},
                                "spending_habits": {
                                    "type": "object",
                                    "properties": {
                                        "fuel": {"type": "integer", "description": "Monthly fuel spending in INR"},
                                        "travel": {"type": "integer", "description": "Monthly travel spending in INR"},
                                        "groceries": {"type": "integer", "description": "Monthly groceries spending in INR"},
                                        "dining": {"type": "integer", "description": "Monthly dining spending in INR"},
                                    },
                                    "required": ["fuel", "travel", "groceries", "dining"],
                                },
                            },
                            "required": ["card_name", "spending_habits"],
                        },
                    },
                },
            ],
        )
        self.thread = self.client.beta.threads.create()

    def process_message(self, message):
        """
        Process a user message and return the assistant's response.
        Args:
            message (str): User's input message.
        Returns:
            str: Assistant's response.
        """
        # Add user message to the thread
        self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=message
        )

        # Create a run
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id
        )

        # Poll for run completion
        while run.status not in ["completed", "failed", "requires_action"]:
            run = self.client.beta.threads.runs.retrieve(run_id=run.id, thread_id=self.thread.id)

        if run.status == "requires_action":
            tool_outputs = []
            for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                # Call appropriate function from CardLogic
                if function_name == "recommend":
                    result = self.card_logic.recommend_cards(arguments)
                elif function_name == "lookup":
                    result = self.card_logic.lookup_card(arguments["card_name"])
                elif function_name == "count":
                    result = self.card_logic.count_cards()
                elif function_name == "profile":
                    self.user_data.update(arguments)
                    result = {"status": "Profile updated"}
                elif function_name == "compare":
                    result = self.card_logic.compare_cards(arguments["card_name1"], arguments["card_name2"])
                elif function_name == "simulate":
                    result = self.card_logic.simulate_rewards(arguments["card_name"], arguments["spending_habits"])
                else:
                    result = {"error": "Unknown function"}

                tool_outputs.append({
                    "tool_call_id": tool_call.id,
                    "output": json.dumps(result)
                })

            # Submit tool outputs
            run = self.client.beta.threads.runs.submit_tool_outputs(
                run_id=run.id,
                thread_id=self.thread.id,
                tool_outputs=tool_outputs
            )

            # Wait for completion
            while run.status not in ["completed", "failed"]:
                run = self.client.beta.threads.runs.retrieve(run_id=run.id, thread_id=self.thread.id)

        # Retrieve and return the latest assistant message
        messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
        for msg in messages.data:
            if msg.role == "assistant":
                return msg.content[0].text.value
        return "Sorry, something went wrong. Please try again."