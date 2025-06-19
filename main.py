import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables from .env
load_dotenv()

# Create the Flask app
app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_DEBUG", "False") == "True")