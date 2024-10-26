import discord
import json

client = discord.Client(intents = discord.Intents.default())

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

with open('/home/samino/Documents/Edupage-Verification-Discord/data/data.json', 'r') as file:
    TOKEN = json.load(file)['BOT_TOKEN']

client.run(TOKEN)