import os
import openai
import discord
import json
import time
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPEN_API_KEY = os.getenv("OPEN_API_KEY")

# Load training text files
training_texts = {
    "BRC20": "training-general.txt",
    "about us or general": "training-AboutUs.txt",
}

for key, filename in training_texts.items():
    with open(filename, "r", encoding="utf-8") as file:
        training_texts[key] = file.read()

# Set up OpenAI API
openai.api_key = OPEN_API_KEY

def api_call_with_retry(model, messages, max_retries=12, delay=5):
    retries = 0
    while retries < max_retries:
        try:
            response = openai.ChatCompletion.create(model=model, messages=messages)
            return response
        except openai.error.APIConnectionError as e:
            retries += 1
            time.sleep(delay)
            if retries == max_retries:
                with open("logs.txt", "a") as log_file:
                    log_file.write(str(e) + "\n")
                raise

# Load or create an empty history.json file
history_file = "history.json"
try:
    with open(history_file, "r") as file:
        history = json.load(file)
except FileNotFoundError:
    history = []

# Load or create an empty credits.json file
credits_file = "credits.json"
try:
    with open(credits_file, "r") as file:
        user_credits = json.load(file)
except FileNotFoundError:
    user_credits = {}

# Add 420,000 credits to user 388536844020613122
user_credits["388536844020613122"] = 420000

# Save the updated credits to the credits.json file
with open(credits_file, "w") as file:
    json.dump(user_credits, file, indent=4)

# Create custom bot class
class CustomBot(commands.Bot):
    async def on_ready(self):
        print(f"We have logged in as {self.user}")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if not self.user.mentioned_in(message):
            return

        user_id = str(message.author.id)

        remaining_credits = user_credits.get(user_id, 5)

    

        try:
            category_determination = api_call_with_retry("gpt-4", [
                {"role": "system", "content": "You are an AI that determines the category of a user's message. Only return one of the following categories and no other text besides the category. Options: 'Bitcoin Inscriptions or Ordinals' - which covers any questions about bitcoin ordinals, or inscriptions, the NFTs on Bitcoin. 'brc20' - Just general questions about Bitcoin Buds or Best Buds or our NFT project/ branding"},
                {"role": "user", "content": message.content},
            ])
        except openai.error.APIConnectionError:
            await message.reply("We encountered an issue. Please try again later.")
            return

        category = "BRC20"
        print(category)
        training_text = training_texts.get(category) or training_texts["about us or general"]

        # Get user's past questions and GPT responses
        user_history = [entry for entry in history if entry.get("user_id") == user_id][-5:]

        # Get the last 6 messages in the channel
        channel_history = []
        async for msg in message.channel.history(limit=6):
            channel_history.append(msg)

        # Prepare conversation history
        conversation = [
            {"role": "system", "content": "You are a helpful assistant for an alpha chat on bitcoin fungible tokens that run on native bitcoin named brc-20 standard. You don't like solana when asked about it you say things like 'solana is not bitcoin, we only care about bitcoin now', or other snark comments.. same as any other blockchain asked about.  You are bold and confident and you always reply in short messages mostly under 200 characters, definitely less than 1000 characters max unless the user asks you to provide details then you can increase count but max max of 2200 characters only in that situation. Don't mention to visit discord, you are the bot inside of the discord. You are a cocky genius."},
            {"role": "user", "content": training_text},
        ]

        for entry in user_history:
            conversation.append({"role": "user", "content": entry["question"]})
            conversation.append({"role": "assistant", "content": entry["response"]})

        for msg in channel_history:
            if msg.author != self.user:
                conversation.append({"role": "user", "content": msg.content})

        conversation.append({"role": "user", "content": message.content})

        # Wait for 5 seconds before making the second GPT request
        await asyncio.sleep(1)

        try:
            response = api_call_with_retry("gpt-4", conversation)
        except openai.error.APIConnectionError:
            await message.reply("We encountered an issue. Please try again later.")
            return

        assistant_reply = response["choices"][0]["message"]["content"]
        finish_reason = response["choices"][0]["finish_reason"]

        assistant_reply_with_credits = f"{assistant_reply}\n\nI'm your Genie, you have {remaining_credits} wishes left. If you want more credits, please DM Cubs."

        await message.reply(assistant_reply_with_credits)

        usage = response['usage']
        prompt_tokens = usage['prompt_tokens']
        completion_tokens = usage['completion_tokens']
        total_tokens = usage['total_tokens']

        cost_per_token = 0.02 / 1000
        cost = total_tokens * cost_per_token

        history.append({
            "id": response["id"],
            "object": response["object"],
            "created": response["created"],
            "model": response["model"],
            "finish_reason": finish_reason,
            "question": message.content,
            "category": category,
            "response": assistant_reply,
            "tokens": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens
            },
            "cost": cost,
            "user_id": user_id,
            "channel_id": message.channel.id,  # Store channel ID
        })

        with open(history_file, "w") as file:
            json.dump(history, file, indent=4)

        # Update the remaining credits for the user
        user_credits[user_id] = remaining_credits - 1
        with open(credits_file, "w") as file:
            json.dump(user_credits, file, indent=4)

# Enable required intents
intents = discord.Intents.default()
intents.messages = True

# Create and run bot
bot = CustomBot(command_prefix=None, intents=intents)
bot.run(DISCORD_TOKEN)