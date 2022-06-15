from bender.chatbot import Config
from bender.gpt import Api
from discord.ext import commands

gpt = Api(Config().load("api.json"))

@commands.command()
async def complete(ctx, *args):
    """
    send a completion request to gpt server
    """
    query = " ".join(args)
    query = {"inputs": query}
    completed_query = await gpt.query(query)
    if isinstance(completed_query, str):
        await ctx.send("```{}```".format(completed_query))
    elif ctx.bot.config["debug"]:
        await ctx.send("`Error: {}`".format(completed_query))

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

def setup(bot):
    bot.add_command(complete)
    bot.add_command(debug)
    bot.add_command(loadcfg)
    bot.add_command(savecfg)
    bot.add_command(reload)