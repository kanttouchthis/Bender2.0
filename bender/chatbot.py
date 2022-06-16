import json
from discord.ext import commands


class Config(dict):
    def __init__(self, filename=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self
        if filename:
            self.load(filename)

    def load(self, filename):
        self.filename = filename
        with open(filename) as f:
            self.update(json.load(f))
        return self
    
    def save(self, filename):
        with open(filename, "w") as f:
            json.dump(self, f, indent=4)
        return self


class Bot(commands.Bot):
    def __init__(self, config:Config=Config(), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.response_bot = None

    async def on_ready(self):
        print("------")
        print("Logged in as")
        print(self.user.name)
        print(self.user.id)
        print("------")
        await self.load_extensions()
    
    async def load_extensions(self):
        for extension in self.config["extensions"]:
            try:
                self.load_extension(extension)
                print(f"Loaded extension: {extension}")
            except Exception as e:
                print(f"Failed to load extension {extension}.")
                print(e)
                raise e
    
    async def reload_extensions(self):
        self.config.load(self.config.filename)
        for extension in self.config["extensions"]:
            try:
                self.reload_extension(extension)
                print(f"Reloaded extension: {extension}")
            except commands.errors.ExtensionNotLoaded:
                self.load_extension(extension)
                print(f"Loaded extension: {extension}")
            except Exception as e:
                print(f"Failed to reload extension {extension}.")
                print(e)
                raise e
    
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.startswith(self.config["command_prefix"]):
            await self.process_commands(message)
            return
        if self.response_bot is not None:
            response = await self.response_bot.respond(message)
            if response is not None:
                await message.channel.send(response)
