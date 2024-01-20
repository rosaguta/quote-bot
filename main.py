import discord
from discord import app_commands
from discord.ext import commands
import requests
import os
from datetime import datetime, timezone, timedelta


class Bot(commands.Bot):
    def __init__(self, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix="!", intents=intents, case_insensitive=True)

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        await self.tree.sync()

    async def on_message(self, message):
        # Check if the bot was mentioned and the message contains a specific emote
        if self.user.mentioned_in(message) and "<:FYOUcat:" in message.content:
            # print(message.content)
            # Respond to the mention with a custom message
            await message.channel.send(f"Well fuck you too {message.author.mention}!")
        
        if self.user.mentioned_in(message) and message.author.id == 235395642623655937:
            await message.channel.send(f"<:FYOUcat:1198281430971727893>")

        # Let the bot process commands as well
        await self.process_commands(message)


intents = discord.Intents.all()
bot = Bot(intents=intents)

async def get_randomquote():
    try:
        response = requests.get("https://quote.digitalindividuals.com/quote")
        response.raise_for_status()
        return response.content.decode()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching quote: {e}")
        return "Failed to fetch quote."



@bot.hybrid_command(name='quote', description="this returns a random quote uwu")
async def quote(interaction: discord.Interaction):
    try:
        quote_content = await get_randomquote()
        await interaction.reply(content=quote_content)
    except Exception as e:
        print(f"Error executing quote command: {e}")
        await interaction.reply(content="Failed to fetch quote. Please try again later.")

@bot.hybrid_command(name='newquote', description='create a new quote urself uwu')
async def newquote(interaction: discord.Interaction ,quote: str, who: str):
    
    headers = {
    'accept': 'text/plain',
    'Content-Type': 'application/json',
    }


    current_utc_time = datetime.utcnow()
    updated_time = current_utc_time + timedelta(hours=1)
    formatted_date = updated_time.replace(microsecond=0).isoformat()
    data = {
        "text": quote,
        "person": who,
        "dateTimeCreated": formatted_date
    }
    response = requests.post("https://quote.digitalindividuals.com/quote", headers=headers, json=data)
    decoded_response = response.content.decode()
    if decoded_response == 'true':
        await interaction.reply(content="quote added ^-^")
    else:
        await interaction.reply(content="something went wrong, blame rose >:3")
        

    
        

token = os.getenv('TOKEN')
bot.run(token)