# Discord Bot for Bitcoin BRC-20 NFT Project

This is a custom Discord bot that utilizes OpenAI's GPT-4 API to answer user questions about the BRC-20 NFT project running on the native Bitcoin blockchain. The bot is designed to be bold, confident, and provide concise responses related to the project, as well as display a particular dislike for non-Bitcoin blockchains such as Solana.

## Features

- Category determination for user messages
- Custom conversation history and user credits system
- Short and informative responses from the AI
- Logging of API errors
- Easy setup with environment variables

## Installation

1. Clone the repository or download the source code.

2. Install the required dependencies:

```
pip install discord.py openai python-dotenv
```

3. Create a `.env` file in the project directory and set the required environment variables:

```
DISCORD_TOKEN=<YOUR_DISCORD_BOT_TOKEN>
OPEN_API_KEY=<YOUR_OPENAI_API_KEY>
```

4. Run the bot:

```
python bot.py
```

## Usage

To communicate with the bot, simply mention it in a message on the Discord server:

```
@Bot What is the BRC-20 standard?
```

The bot will then respond with a short and informative answer.

## Files

- `bot.py`: The main bot script that connects to Discord and handles user messages with GPT-4 API calls.
- `history.json`: Stores the conversation history for each user on the server.
- `credits.json`: Stores the number of remaining credits for each user on the server.
- `logs.txt`: Logs any API errors encountered during execution.
- `.env`: Contains the environment variables needed for the bot to run (Discord token and OpenAI API key).
- `training-*.txt`: Training text files used by the bot to answer user questions related to specific categories.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.
