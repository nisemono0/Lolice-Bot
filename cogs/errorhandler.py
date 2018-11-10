
import logging

import discord
from discord.ext import commands


class CommandErrorHandler:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, context, error):
        # Ignore if command is not found or if command had user input error
        ignored = (commands.CommandNotFound, commands.UserInputError)
        if isinstance(error, ignored):
            return
        # Ignore BadArgument errors
        elif isinstance(error, commands.BadArgument):
            return
        # Ignore PM commands
        elif isinstance(error, commands.NoPrivateMessage):
            return
        elif isinstance(error, commands.CommandInvokeError):
            print(f'{error.original.__class__.__name__}: {error.original}')
            logging.error((f'{error.original.__class__.__name__}: {error.original}').encode("utf-8"))
    
def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
