from Verification.Verification import Verification
import discord, os, json, aiohttp, logging



# A Discord bot class that handles various events such as member joining, message receiving, and image downloading.
# Attributes:
#     BASE_DIR (str): The base directory of the bot.
#     bot_data (dict): The bot's configuration data loaded from a JSON file.
#     roles (dict): The roles configuration data loaded from a JSON file.
#     verification (Verification): An instance of the Verification class.
#     client (discord.Client): The Discord client instance with specified intents.
# Methods:
#     __init__(): Initializes the bot, sets up permissions, and starts the bot.
#     get_bot_data(): Loads and returns the bot's configuration data from a JSON file.
#     get_roles(): Loads and returns the roles configuration data from a JSON file.
#     get_token(): Retrieves the bot token from a JSON file.
#     on_ready(): Event handler for when the bot is ready.
#     on_member_join(member): Event handler for when a new member joins the server.
#     on_message(message): Event handler for when a message is received.
#     add_role_to_member(guild, member, role_name): Adds a role to a member after verification.
#     set_member_nickname(guild, member, nickname): Sets the nickname of a member after verification.
#     download_image(url, filename): Downloads an image from a given URL and saves it to a specified filename.
#     delete_image(filename): Deletes an image with a specified filename.

class Bot():
    

    #initialize bot
    def __init__(self) -> None:
        self.BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.bot_data = self.get_bot_data()
        self.roles = self.get_roles()
        self.verification = Verification()

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
        self.logging.basicConfig(
            level=logging.DEBUG,  # Log all levels from DEBUG and above
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.joing(self.BASE_DIR, "debug.log")),  # Log to a file called bot.log
                logging.StreamHandler()          # Also log to the console
            ]
        )
        


    #get needed information from .json
    def get_bot_data(self) -> dict:
        with open(os.path.join(self.BASE_DIR, 'Bot', 'Bot_data.json'), 'r') as file:
            return json.load(file)
    
    # get roles from .json file
    def get_roles(self) -> dict:
        with open(os.path.join(self.BASE_DIR, 'Bot', 'Roles.json'), 'r') as file:
            return json.load(file)


    #get bot token from .json file
    def get_token(self) -> str:
        file_path = os.path.join(self.BASE_DIR, 'data', 'data.json')
        with open(file_path, 'r') as file:
            return json.load(file)['BOT_TOKEN']
    
    #check if bot is online
    async def on_ready(self) -> None:
        self.logger = logging.getLogger("discord_bot")
        self.logger.info(f'We have logged in as {self.client.user}')

    #detect member join and send welcome mesage
    async def on_member_join(self, member: discord.Member) -> None:
        WELCOME_MSG = self.bot_data['WELCOME_MSG']
        PC_MSG = "Ak overenie robíš na PC/Laptope: :computer:"
        MOBILE_MSG = "Ak overenie robíš na mobile: :iphone:"
        PC_IMG = os.path.join(self.BASE_DIR, 'Bot', self.bot_data['PC_IMG'])
        MOBILE_IMG = os.path.join(self.BASE_DIR, 'Bot', self.bot_data['MOBILE_IMG'])
        try:
            await member.send(f"{WELCOME_MSG} \n\n {PC_MSG} \n {MOBILE_MSG}" , files = [discord.File(PC_IMG), discord.File(MOBILE_IMG)])

        except discord.Forbidden:
            self.logger.error(f'Could not send a message to {member}')

        except Exception as e:
            self.logger.error(f'An error occured: {e}')

    #detect message receive
    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.client.user:
            return

        #check if DM attachment
        if isinstance(message.channel, discord.DMChannel) and message.attachments:
            await message.channel.send(f"Sprava prijata, overujem...")

            #download images
            if len(message.attachments) > 1:
                await message.channel.send("Posielaj len jednu fotku naraz :x:")
                return
            
            for i,attachment in enumerate(message.attachments):
                if attachment.content_type and 'image' in attachment.content_type:
                    filename = f"{str(message.author)}-{i}.{attachment.filename.split('.')[-1]}"
                    await self.download_image(attachment.url, filename)
                    member_status = self.verification.verify(filename)
                    if member_status['STATUS']:
                        await message.channel.send(f"Člen {member_status['NAME']} je študentom a si verifikovaný. :white_check_mark:")

                        # Add role after verification
                        guild = discord.utils.get(self.client.guilds)
                        await self.add_role_to_member(guild, message.author, self.roles[member_status['CLASS']])
                        # Set nickname after verification
                        await self.set_member_nickname(guild, message.author, member_status['NAME'])

                    else:
                        await message.channel.send(f"Nastala chyba {member_status['ERROR']} a nie si verifikovaný :x: :cry:")
                        self.logger.error(f"Verification failed for {message.author}: {member_status['ERROR']}")
                    self.delete_image(filename)
    
    # Add role to member after verification
    async def add_role_to_member(self, guild: discord.Guild, member: discord.User, role_name: str) -> None:
        role = discord.utils.get(guild.roles, name=role_name)
        if role is None:
            self.logger.error(f"Role '{role_name}' not found.")
            return
        
        guild_member = guild.get_member(member.id)
        if guild_member is None:
            self.logger.error(f"User {member} not found in the guild.")
            return

        try:
            await guild_member.add_roles(role)

        except discord.Forbidden:
            self.logger.error("Bot does not have permission to assign roles.")
        except Exception as e:
            self.logger.error(f"Failed to assign role due to an exception: {e}")

    # Set nickname to member after verification
    async def set_member_nickname(self, guild: discord.Guild, member: discord.User, nickname: str) -> None:
        guild_member = guild.get_member(member.id)
        if guild_member is None:
            self.logger.error(f"User {member} not found in the guild.")
            return

        try:
            await guild_member.edit(nick=nickname)

        except discord.Forbidden:
            self.logger.error("Bot does not have permission to manage nicknames.")
        except Exception as e:
            self.logger.error(f"Failed to set nickname due to an exception: {e}")

    # Download image from URL
    async def download_image(self, url: str, filename: str) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    file_path = os.path.join(self.BASE_DIR, 'images', filename)
                    with open(file_path, "wb") as f:
                        f.write(image_data)
    
    # Delete image after verification
    def delete_image(self, filename: str) -> None:
        file_path = os.path.join(self.BASE_DIR, 'images', filename)
        os.remove(file_path)
