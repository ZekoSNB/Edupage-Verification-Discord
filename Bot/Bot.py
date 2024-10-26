import discord
import json


class Bot():
    def __init__(self):
        self.client = discord.Client(intents = discord.Intents.default())
        self.client.event(self.on_ready)
        self.client.run(self.get_token())

    def get_token(self):
        with open('/home/samino/Documents/Edupage-Verification-Discord/data/data.json', 'r') as file:
            return json.load(file)['BOT_TOKEN']
        
    
    async def on_ready(self):
        print(f'We have logged in as {self.client.user}')



if __name__ == '__main__':
    Bot()