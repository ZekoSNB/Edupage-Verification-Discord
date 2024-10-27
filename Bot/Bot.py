import discord
import os
import json


class Bot():
    def __init__(self):
        self.BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.bot_data = self.get_bot_data()
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        self.client = discord.Client(intents = intents)
        self.client.event(self.on_ready)
        self.client.event(self.on_member_join)
        self.client.run(self.get_token())

    def get_bot_data(self):
        with open(os.path.join(self.BASE_DIR, 'Bot', 'Bot_data.json'), 'r') as file:
            return json.load(file)

    def get_token(self):
        file_path = os.path.join(self.BASE_DIR, 'data', 'data.json')
        with open(file_path, 'r') as file:
            return json.load(file)['BOT_TOKEN']
    
    async def on_ready(self):
        print(f'We have logged in as {self.client.user}')

    async def on_member_join(self, member):

        WELCOME_MSG = self.bot_data['WELCOME_MSG']
        PC_MSG = "Ak overenie robíš na PC/Laptope: :computer:"
        MOBILE_MSG = "Ak overenie robíš na mobile: :iphone:"
        PC_IMG = os.path.join(self.BASE_DIR, 'Bot', self.bot_data['PC_IMG'])
        MOBILE_IMG = os.path.join(self.BASE_DIR, 'Bot', self.bot_data['MOBILE_IMG'])

        print(f"Sending message to {member}...")
        try:
            await member.send(f"{WELCOME_MSG} \n\n {PC_MSG} \n {MOBILE_MSG}" , files = [discord.File(PC_IMG), discord.File(MOBILE_IMG)])
        except discord.Forbidden:
            print(f'Could not send a message to {member}')
        except Exception as e:
            print(f'An error occured: {e}') 


if __name__ == '__main__':
    Bot()