from flask import Flask, render_template, request, jsonify
from agents.base_agent import CreditCardAssistant
import os

def create_app():
    app = Flask(__name__)
    assistant = None

    def initialize_assistant():
        nonlocal assistant
        assistant = CreditCardAssistant()

    initialize_assistant()

    @app.route("/")
    def index():
        """Render the chat UI."""
        return render_template("index.html")

    @app.route("/chat", methods=["POST"])
    def chat():
        """Handle user messages and return assistant responses."""
        try:
            user_message = request.json.get("message")
            if not user_message:
                return jsonify({"error": "No message provided"}), 400

            # Process the message through the assistant
            response = assistant.process_message(user_message)
            return jsonify({"response": response})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/reset", methods=["POST"])
    def reset():
        """Reset the assistant for a new conversation."""
        try:
            initialize_assistant()
            return jsonify({"status": "Conversation reset"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app