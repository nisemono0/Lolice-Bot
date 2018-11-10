import logging

import discord
from discord.ext import commands

from CustomImports import variables


class OtherCommands():
    """Other Commands"""
    def __init__(self, bot):
        self.bot = bot
    
    def pervert_check(self):
        def predicate(context):
            user_roles = [role.name for role in context.message.author.roles]
            if variables.not_verified in user_roles:
                return False
            else:
                return True
        return commands.check(predicate)

    @commands.command(pass_context=True)
    @pervert_check(None)
    async def pervert(self, context):
        """$pervert: Gives or removes the NSFW role"""
        nsfw_role = discord.utils.get(context.message.author.server.roles, name=variables.nsfw_role)
        user_roles = [role.name for role in context.message.author.roles]
        if variables.nsfw_role in user_roles:
            await self.bot.remove_roles(context.message.author, nsfw_role)
        else:
            await self.bot.add_roles(context.message.author, nsfw_role)

def setup(bot):
    bot.add_cog(OtherCommands(bot))
