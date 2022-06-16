import aiohttp
from bender.chatbot import Config

class Bender:
    def __init__(self, config:Config=Config()):
        self.config = config
    
    async def response(self, query):
        url = self.config["api_url"] + "/response"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=query) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print("API Error: {}".format(response.status))
                return response.status

    async def reset(self):
        url = self.config["api_url"] + "/reset"
        async with aiohttp.ClientSession() as session:
            async with session.post(url) as response:
                if response.status == 200:
                    return True
                else:
                    print("API Error: {}".format(response.status))
                return 0

    async def get_response(self, text):
        query = {"text": text, "episode_done": False}
        completed_query = await self.response(query)
        if isinstance(completed_query, int) and self.config["debug"]:
            return "`Error: {}`".format(completed_query)
        else:
            completed_query = completed_query["response"]
            return completed_query
    
    async def respond(self, message):
        return await self.get_response(message.content)


def setup(bot):
    bot.response_bot = Bender(Config().load("bender.json"))