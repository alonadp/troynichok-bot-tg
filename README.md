# troynichok-bot-tg
Telegram bot for daily predictions
## Description
**Troynichok** is a **Telegram bot** that sends daily predictions and can engage in philosophical conversations with users. The bot is written in Python and uses **OpenAI GPT** to generate texts and responses.
### Features:
* **Daily Predictions**: The bot sends users random philosophical predictions every day.
* **Conversations with the Bot**: The bot can answer questions and engage in conversations, thanks to integration with OpenAI.
* **Command Management**: You can manage the bot using simple commands in the chat.
* **Flexible Configuration**: You can set the prediction sending time, logging level, and other parameters.

## Installation and Setup

### 1. Clone the Repository

Start by cloning this repository to your local machine using Git:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

## Install Dependencies

Before running the bot, you need to install all the dependencies listed in the project. To do this, run the command:

```bash
pip install -r requirements.txt
```

## Create Configuration File

You need to create a configuration file `config.py` where the data required for the bot's operation will be stored (such as the Telegram token and the OpenAI API key).

1. Create the `config.py` file in the root of the project.
2. Add the following configuration settings:

```python
# Telegram bot token
TOKEN = "your token here"

# OpenAI API key
OPENAI_API_KEY = "your-api-key-here"

# Bot username (including "bot" at the end)
BOT_USERNAME = "mainadminnbot"

# List of user IDs who will be admins
ADMIN_IDS = []

# API request settings
REQUEST_TIMEOUT = 30  # API response timeout in seconds

# Scheduling settings
PREDICTION_TIME = "09:00"  # Time for sending daily predictions

# Logging settings
LOG_LEVEL = "INFO"  # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_FILE = "bot.log"

# List of allowed chat IDs
ALLOWED_CHAT_IDS = []
```

## Replace the placeholders with your data:

* **TOKEN**: Get the token for your bot via [BotFather](https://core.telegram.org/bots#botfather).
* **OPENAI\_API\_KEY**: Get your API key from [OpenAI](https://platform.openai.com/signup).
* **BOT\_USERNAME**: Enter your bot's name in Telegram (it should end with "bot").
* **ADMIN\_IDS**: Add the user IDs of those who will be admins.

## Running the Bot

Now that the configuration file is set up, you can run the bot. To do this, execute the command:

```bash
python bot.py
```

