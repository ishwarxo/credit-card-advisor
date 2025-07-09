## Overview

The Credit Card Recommender is a web-based application designed to assist users in finding the best credit card options based on their financial preferences, such as monthly income, spending habits, and desired rewards. Built with Python and Flask, it features a dynamic chat interface inspired by SimpleChat, allowing real-time interaction with personalized recommendations. The app includes a sticky footer with links to the developer's profiles and is deployed on Render for public access.

## Features

Interactive Chat Interface: Users can input preferences (e.g., income, spending) via a chat box with blue user bubbles and gray bot responses.
Personalized Recommendations: Leverages a JSON dataset and AI API integration to suggest credit cards with details like rewards and key reasons.
Responsive Design: Optimized for desktop and mobile with a SimpleChat-like UI, including a loading spinner and fixed footer.
User Experience Enhancements: Supports Enter key for sending messages, conversation restart/clear options, and Markdown-formatted responses with images.
Deployment: Hosted on Render with GitHub integration, adapting to free tier constraints.

## Technologies

Backend: Python, Flask, Gunicorn
Frontend: HTML, CSS (Bootstrap), JavaScript (Marked.js for Markdown parsing)
Version Control: Git, GitHub
Deployment: Render
Data: JSON (cards.json)
Additional Tools: Environment variables for API keys

## Installation Prerequisites

Python 3.10 or higher
Git
Internet connection for dependencies and deployment

Clone the Repository
git clone https://github.com/your-username/credit-card-advisor.git
cd credit-card-advisor

Set Up Virtual Environment
python -m venv venv
venv\Scripts\activate  # On Windows

Install Dependencies
pip install -r requirements.txt


Ensure requirements.txt includes flask, gunicorn, and any API libraries (e.g., openai).

## Configure Environment Variables

Create a .env file in the root directory:
OPENAI_API_KEY=your-api-key


Note: .env is ignored by Git (see .gitignore).


## Usage
Run Locally
python main.py


Open http://localhost:5000 in your browser.
Start by entering your monthly income (e.g., "50000") when prompted, followed by spending details and preferences (e.g., "travel_points", "none", "750").
Send messages using the "Send" button or Enter key.
Use "Start Over" or "Clear Chat" to reset the conversation.

## Example Interaction

User: "Recommend a card"
Bot: "Please provide your monthly income in INR."
User: "50000"
Bot: "Great! How much do you spend monthly?..."
(After inputs) Bot: "Here are the recommended credit cards: [list with Rewards, images]..."

## Deployment Steps

Push to GitHub:
git add .
git commit -m "Update for deployment"
git push origin main


Set Up Render:

Sign up at render.com.
Create a new Web Service, connect your GitHub repo.
Configure:
Build Command: pip install -r requirements.txt
Start Command: gunicorn --bind 0.0.0.0:$PORT main:app
Environment: Add OPENAI_API_KEY as a variable.


Deploy and note the provided URL.


Verify: Test the live app and monitor logs via the Render Dashboard.


## File Structure
credit-card-advisor/
├── main.py              # Runs the Flask app
├── app.py              # Defines the Flask app instance
├── .env                # Environment variables (ignored)
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── Procfile           # Deployment command
├── render.yaml        # Render configuration (optional)
├── venv               # Virtual environment (ignored)
├── data/
│   └── cards.json     # Credit card data
├── services/
│   └── card_logic.py  # Business logic
├── agents/
│   ├── base_agent.py  # AI agent logic
│   └── tools/
│       └── recommend.py
├── templates/
│   └── index.html     # Main HTML template
├── cards/
│   ├── lookup.py      # Card lookup functions
│   ├── count.py       # Card counting logic
│   ├── profile.py     # Card profile generation
│   ├── compare.py     # Card comparison
│   └── simulate.py    # Reward simulation
├── static/
│   └── styles.css     # Custom CSS

## Contributing

Fork the repository.
Create a new branch: git checkout -b feature-branch.
Make changes and commit: git commit -m "Describe changes".
Push to GitHub: git push origin feature-branch.
Submit a pull request for review.

License

MIT License (Add a LICENSE file if desired, e.g., using echo "MIT License" > LICENSE).

## Acknowledgements

Inspired by SimpleChat design principles.
Utilized Bootstrap and Marked.js for rapid development.
Deployed on Render with community support.

## Contact

Email: ishwar.kumar144014@gmail.com
LinkedIn: https://www.linkedin.com/in/ishwar-kumar-pal/
GitHub: https://github.com/ishwarxo


## Demo
[Drive Link](https://drive.google.com/file/d/15824bSllRF6xPnak0SkMzX3ZPZ_0wPmd/view?usp=sharing)

## Deployment
Deployed on [https://credit-card-advisor-6gdk.onrender.com/](https://credit-card-advisor-6gdk.onrender.com/)