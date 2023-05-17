
#GPT-4 Based Discord Bot
This codebase comprises of a custom Discord bot that utilizes OpenAI's GPT-4 model to interact with users. The bot identifies the category of a user's message, and based on the category, it responds appropriately. It has a system of user credits, maintains a conversation history, and can handle API errors.

Installation
Before you begin, make sure you have Python 3.7 or above installed.

Clone this repository.

Install the required Python packages by running:

sh
Copy code
pip install -r requirements.txt
This command installs the following packages:

discord
openai
python-dotenv
asyncio
Create a .env file in the root directory of the project, and add the following environment variables:

sh
Copy code
DISCORD_TOKEN=<Your Discord Bot Token>
OPEN_API_KEY=<Your OpenAI API Key>
Create a training-general.txt file and a training-AboutUs.txt file in the root directory of the project. These files should contain the training texts for the bot.

Create an empty history.json file and credits.json file in the root directory of the project.

Usage
Run the bot using the following command:

sh
Copy code
python bot.py
The bot will now be active on your Discord server.

Features
The bot uses OpenAI's GPT-4 model to interpret and respond to user messages.
It maintains a history of user conversations and uses it to provide context-aware responses.
It handles OpenAI API errors gracefully by retrying API calls and logging errors.
It maintains a credit system for users and updates the remaining credits after each interaction.
It also logs the cost of each conversation in terms of tokens used in the GPT-4 model.
The bot's responses are based on predefined categories of the user's messages.
Notes
The bot only responds to messages where it is mentioned.
The bot is designed to be a bit cocky and confident, often replying in short messages and making snarky comments about non-bitcoin blockchains.
The bot operates within a maximum character limit for its responses unless asked to provide more details.
The api_call_with_retry function is set to retry a maximum of 12 times with a delay of 5 seconds between retries. You can adjust these parameters as needed.
The bot can manage user credits. Every user starts with 5 credits, and each interaction costs 1 credit. Users can earn more credits (shown in the code where user "388536844020613122" gets 420000 credits).
The bot uses a predefined cost per token for calculating the cost of a conversation.
Disclaimer
This bot interacts with users based on the training it has received. While it has been designed to behave in a certain way, the nature of AI means that its responses may not always be predictable. Please use this bot responsibly and monitor its interactions to ensure they are in line with your community's guidelines.
