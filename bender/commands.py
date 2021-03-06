from bender.chatbot import Config
from discord.ext import commands
import aiohttp
import json
import sys


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
                    return await response.json()
                else:
                    print("API Error: {}".format(response.status))
                return response.status


try:
    gpt = Api(Config().load("gpt.json"))
    t5 = Api(Config().load("t5.json"))
except:
    pass

@commands.command()
async def complete(ctx, *args):
    """
    send a completion request to gpt server
    """
    query = " ".join(args)
    query = {"inputs": query, "wait_for_model": True}
    completed_query = await t5.query(query)
    if isinstance(completed_query, int) and ctx.bot.config["debug"]:
        await ctx.send("`Error: {}`".format(completed_query))
    else:
        completed_query = completed_query[0]['generated_text']
        await ctx.send("```{}```".format(completed_query))


@commands.command()
async def translate(ctx, *args):
    """
    send a translation request to t5 server
    """
    query = " ".join(args)
    query = {"inputs": query, "wait_for_model": True}
    completed_query = await t5.query(query)
    if isinstance(completed_query, int) and ctx.bot.config["debug"]:
        await ctx.send("`Error: {}`".format(completed_query))
    else:
        completed_query = completed_query[0]['translation_text']
        await ctx.send("```{}```".format(completed_query))

@commands.command()
async def clearhistory(ctx):
    """
    clear the history of the bot
    """
    if ctx.bot.response_bot is not None:
        await ctx.bot.response_bot.reset()
        await ctx.send("`History cleared`")

@commands.command()
@commands.has_permissions(administrator=True)
async def debug(ctx, *, debug: bool=None):
    """
    enable/disable debug mode
    """
    if isinstance(debug, bool): ctx.bot.config["debug"] = debug
    await ctx.send("`Debug: {}`".format(ctx.bot.config["debug"]))

@commands.command()
@commands.has_permissions(administrator=True)
async def loadcfg(ctx, *, filename: str=None):
    """
    load a config file
    """
    if filename is None: filename = ctx.bot.config.filename
    ctx.bot.config.load(filename)
    await ctx.send("`Loaded config: {}`".format(filename))

@commands.command()
@commands.has_permissions(administrator=True)
async def savecfg(ctx, *, filename: str=None):
    """
    save a config file
    """
    if filename is None: filename = ctx.bot.config.filename
    ctx.bot.config.save(filename)
    await ctx.send("`Saved config: {}`".format(filename))

@commands.command()
@commands.has_permissions(administrator=True)
async def reload(ctx):
    """
    reload all extensions
    """
    await ctx.bot.reload_extensions()
    await ctx.send("`Reloaded extensions`")

@commands.command()
@commands.has_permissions(administrator=True)
async def stop(ctx):
    """
    stop the bot
    """
    await ctx.send("`Stopping`")
    sys.exit(0)

def setup(bot):
    bot.add_command(complete)
    bot.add_command(translate)
    bot.add_command(clearhistory)
    bot.add_command(debug)
    bot.add_command(loadcfg)
    bot.add_command(savecfg)
    bot.add_command(reload)
    bot.add_command(stop)