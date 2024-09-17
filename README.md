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


## Google Cloud Authentication Setup

To set up Google Cloud authentication for accessing the Google Sheets API, follow these steps:

1. **Create a Google Cloud Project**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Click on "Select a Project" and then "New Project."
   - Enter a project name and click "Create."

2. **Enable the Google Sheets API**:
   - In the Google Cloud Console, navigate to the "APIs & Services" > "Library."
   - Search for "Google Sheets API" and click on it.
   - Click "Enable" to activate the API for your project.

3. **Create a Service Account**:
   - Go to "APIs & Services" > "Credentials."
   - Click on "Create Credentials" and select "Service Account."
   - Fill in the service account name and description, then click "Create."
   - On the next page, click "Done."

4. **Create a JSON Key**:
   - Find your newly created service account in the list and click on it.
   - Click on the "Keys" tab, then "Add Key" > "Create New Key."
   - Choose "JSON" and click "Create." This will download a JSON file containing your service account credentials.

5. **Share the Google Sheet**:
   - Open your Google Sheet (request yeomenghan1989@gmail.com for a sample google sheet format).
   - Click the "Share" button.
   - Add the service account email (found in the downloaded JSON file) with at least "Viewer" permissions.

6. **Set Up Environment Variable**:
   - Copy the contents of the JSON file and set it in your `.env` file as follows:

   ```plaintext
   GOOGLE_KEY='{"type": "service_account", "project_id": "your-project-id", ...}'
   ```

## Telegram Bot Setup with BotFather

This document outlines the steps to create a Telegram bot using BotFather and obtain the necessary API token for your bot.

1. Open Telegram

    Launch the Telegram app or visit the [Telegram Web](https://web.telegram.org/) interface.

2. Find BotFather
  - In the search bar, type `@BotFather`.
  - Click on the BotFather bot to open a chat.

3. Start a New Bot
  - Send the command `/newbot` to BotFather.
  - Follow the prompts:
    - **Choose a name** for your bot (this can be anything you like).
    - **Choose a username** for your bot (must end with `bot`, e.g., `example_bot`).

4. Receive Your API Token
  - After successfully creating the bot, BotFather will provide you with an **API token**.
  - **Keep this token safe**, as it is required for your bot to authenticate with the Telegram API.

5. Set Up Environment Variable

  - Store your API token in your project’s `.env` file (or any configuration method you prefer) as follows:

    ```plaintext
    API_KEY=your_telegram_bot_api_token
    ```

## Project Setup

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
