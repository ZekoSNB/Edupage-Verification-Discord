import discord
import os
import json
import aiohttp

class Bot():

    #initialize bot
    def __init__(self):
        self.BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.bot_data = self.get_bot_data()

        #giving bot permissions
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        self.client = discord.Client(intents = intents)

        #looking for specific events and running bot with token
        self.client.event(self.on_ready)
        self.client.event(self.on_member_join)
        self.client.event(self.on_message)
        self.client.run(self.get_token())


    #get needed information from .json
    def get_bot_data(self):
        with open(os.path.join(self.BASE_DIR, 'Bot', 'Bot_data.json'), 'r') as file:
            return json.load(file)

    #get bot token from .json file
    def get_token(self):
        file_path = os.path.join(self.BASE_DIR, 'data', 'data.json')
        with open(file_path, 'r') as file:
            return json.load(file)['BOT_TOKEN']
    
    #check if bot is online
    async def on_ready(self):
        print(f'We have logged in as {self.client.user}')

    #detect member join and send welcome mesage
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

    #detect message receive
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        #check if DM attachment
        if isinstance(message.channel, discord.DMChannel) and message.attachments:
            print(f'{message.author} sent a message: {message.content}, {len(message.attachments)} attachments available')
            await message.channel.send(f"Sprava '{message.content}' prijata, {len(message.attachments)} obrazkov.")
           
            #check sent images
            for attachment in message.attachments:
                if attachment.content_type and 'image' in attachment.content_type:
                    print(f"Image '{attachment.filename}' is downloading.")
                    await self.download_image(attachment.url, attachment.filename)
                    await message.channel.send(f"Image '{attachment.filename}' has been downloaded.")

    #download image
    async def download_image(self, url, filename):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    with open(filename, "wb") as f:
                        f.write(image_data)
                    print(f"'{filename}' downloaded.")

if __name__ == '__main__':
    Bot()