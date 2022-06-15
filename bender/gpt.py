import aiohttp
import json


class Api():
    def __init__(self, config:dict):
        self.config = config
    
    async def query(self, query):
        url = self.config["api_url"]
        token = self.config["api_token"]
        headers = {"Authorization": f"Bearer {token}"}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=json.dumps(query), headers=headers) as response:
                if response.status == 200:
                    return (await response.json())[0]['generated_text']
                else:
                    print("API Error: {}".format(response.status))
                return response.status
