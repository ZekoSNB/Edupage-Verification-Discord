import discord
import json

class Bot():
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        self.client = discord.Client(intents = intents)
        self.client.event(self.on_ready)
        self.client.event(self.on_member_join)
        self.client.run(self.get_token())


    def get_token(self):
        with open('/home/samino/Documents/Edupage-Verification-Discord/data/data.json', 'r') as file:
            return json.load(file)['BOT_TOKEN']
        
    def get_wellcome_msg(self):
        with open('/home/samino/Documents/Edupage-Verification-Discord/Bot/msgs.json', 'r') as file:
            return json.load(file)['WELLCOME_MSG']
        
    def get_tpc_img(self):
        return('/home/samino/Documents/Edupage-Verification-Discord/Bot/IMG_3118.JPG')

    def get_tmp_img(self):
        return('/home/samino/Documents/Edupage-Verification-Discord/Bot/IMG_3118.JPG')
    
    async def on_ready(self):
        print(f'We have logged in as {self.client.user}')

    async def on_member_join(self, member):
        print(f"Sending message to {member}...")
        try:
            await member.send(self.get_wellcome_msg())
            await member.send(file = discord.File(self.get_img()))
            print(f"Message sent to {member}")
        except discord.Forbidden:
            print(f'Could not send a message to {member}')
        except Exception as e:
            print(f'An error occured: {e}') 

if __name__ == '__main__':
    Bot()