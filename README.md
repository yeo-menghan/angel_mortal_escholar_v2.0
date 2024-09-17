# Angel & Mortal Telegram Bot

A Telegram bot for the Angel & Mortal game, where participants can communicate anonymously with their assigned "angel" or "mortal." The bot manages user interactions and tracks data using Google Sheets.

Developed using the latest v20 version of python telegram bot: https://github.com/python-telegram-bot/python-telegram-bot

## Features

- User registration and chat initiation
- Anonymous messaging between participants
- Game instructions and announcements
- Google Sheets integration for data storage and retrieval

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.9 or later
- A Telegram Bot API token (from [BotFather](https://core.telegram.org/bots#botfather))
- Google Cloud account with access to Google Sheets API
- A service account with `creds.json` containing your Google Sheets credentials

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/angel-mortal-bot.git
   cd angel-mortal-bot
   ```

2. **Create a virtual environment (optional but recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Create Environment Variables**
    Create a .env file in the project root:
    ```bash
    API_KEY=your_telegram_bot_api_key
    GOOGLE_KEY='your_google_service_account_credentials_json_string'
    ANGEL_BOT_TOKEN=your_angel_bot_token
    ```

5. **Set up Google Sheet**

    Create a Google Sheet for the game and share it with your service account email.
    Ensure your sheet has the necessary columns to store user data.

6. **Run the Bot (locally)**

    ```bash
    python bot.py
    ```


7. **Deploy Bot on Heroku / Google Cloud / AWS**


## Usage

1. Start the bot on Telegram by sending the /start command.
2. Use commands like /angel, /mortal, /help, and /checkinfo to interact with the bot.
3. Participants will be paired with an angel and a mortal (as per the pairings on google sheet), allowing anonymous communication.


## Contributing
Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Make your changes.
4. Commit your changes (git commit -m 'Add new feature').
5. Push to the branch (git push origin feature-branch).
6. Open a pull request.


## License

## Acknowledgments
- python-telegram-bot for the Telegram Bot API wrapper.
- gspread for interacting with Google Sheets.
