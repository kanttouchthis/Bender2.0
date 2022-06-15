from bender.chatbot import Bot, Config

if __name__ == "__main__":
    CONFIG = Config().load("bender.json")
    bot = Bot(CONFIG, command_prefix=CONFIG["command_prefix"])
    bot.run(bot.config["token"])